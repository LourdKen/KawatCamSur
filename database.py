"""
KawatCamSur - database helper module (SQLite, standard library only).

Usage from any page:
    from database import init_db, authenticate_user, list_venues
    init_db()   # call once at app startup
"""

import hashlib
import hmac
import secrets
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "kawatcamsur.db"

# Looks for the schema in these places, in order. Adjust if yours lives elsewhere.
SCHEMA_CANDIDATES = [
    BASE_DIR / "data" / "schema.sql",
    BASE_DIR / "schema.sql",
]

DEFAULT_SPORTS = [
    "Basketball", "Volleyball", "Badminton", "Football", "Table Tennis",
    "Tennis", "Swimming", "Running", "Cycling", "Futsal",
]

PBKDF2_ITERATIONS = 200_000

# Role-based access control: which actions each role may do.
# New signups always get the 'user' role.
ROLE_PERMISSIONS = {
    "user": {
        "add_venue", "add_review", "create_post", "join_post",
    },
    "admin": {
        "add_venue", "add_review", "create_post", "join_post",
        "approve_venue", "manage_users", "view_audit_log",
    },
}


# -----------------------------------------------------
# Connection and setup
# -----------------------------------------------------
def get_connection() -> sqlite3.Connection:
    """Open a connection with foreign keys on and rows accessible by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(seed_sports: bool = True) -> None:
    """Create all tables (safe to call every startup) and seed the sports list."""
    schema_file = next((p for p in SCHEMA_CANDIDATES if p.exists()), None)
    if schema_file is None:
        raise FileNotFoundError(
            "schema.sql not found. Looked in: "
            + ", ".join(str(p) for p in SCHEMA_CANDIDATES)
        )
    with get_connection() as conn:
        conn.executescript(schema_file.read_text(encoding="utf-8"))
        if seed_sports:
            conn.executemany(
                "INSERT OR IGNORE INTO sports (name) VALUES (?)",
                [(s,) for s in DEFAULT_SPORTS],
            )


# -----------------------------------------------------
# Password hashing
# -----------------------------------------------------
def _hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), PBKDF2_ITERATIONS
    ).hex()
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${digest}"


def _verify_password(password: str, stored: str) -> bool:
    try:
        _, iterations, salt, digest = stored.split("$")
        check = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iterations)
        ).hex()
        return hmac.compare_digest(check, digest)
    except (ValueError, AttributeError):
        return False


# -----------------------------------------------------
# Audit log
# -----------------------------------------------------
def log_event(action, user_id=None, entity_type=None, entity_id=None, details=None) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_events (user_id, action, entity_type, entity_id, details) "
            "VALUES (?, ?, ?, ?, ?)",
            (user_id, action, entity_type, entity_id, details),
        )


# -----------------------------------------------------
# Role-based access control (RBAC)
# -----------------------------------------------------
def get_role(user_id):
    """Role of a user, read from the database (so a page cannot fake it)."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT role FROM users WHERE user_id = ?", (user_id,)
        ).fetchone()
    return row["role"] if row else None


def has_permission(user_id, permission) -> bool:
    return permission in ROLE_PERMISSIONS.get(get_role(user_id), set())


def require_permission(user_id, permission) -> None:
    """Raise PermissionError (and log it) if the user may not do this."""
    role = get_role(user_id)
    if permission not in ROLE_PERMISSIONS.get(role, set()):
        # an unknown user id cannot be stored as a foreign key, so log it as NULL
        log_event(
            "permission_denied",
            user_id if role else None,
            details=permission if role else f"{permission} (unknown user id {user_id})",
        )
        raise PermissionError("You don't have permission to do that.")


def make_first_admin(email) -> None:
    """One-time setup. Works only while there is no admin yet."""
    with get_connection() as conn:
        if conn.execute("SELECT 1 FROM users WHERE role = 'admin'").fetchone():
            raise ValueError("An admin already exists.")
        cur = conn.execute(
            "UPDATE users SET role = 'admin' WHERE email = ?", (email.strip().lower(),)
        )
        if cur.rowcount == 0:
            raise ValueError("No user with that email. Sign up first.")
        user_id = conn.execute(
            "SELECT user_id FROM users WHERE email = ?", (email.strip().lower(),)
        ).fetchone()["user_id"]
    log_event("first_admin_created", user_id, "user", user_id)


def set_user_role(acting_user_id, target_user_id, new_role) -> None:
    """Admins only. The last remaining admin cannot be demoted."""
    require_permission(acting_user_id, "manage_users")
    if new_role not in ROLE_PERMISSIONS:
        raise ValueError("Unknown role.")
    with get_connection() as conn:
        target = conn.execute(
            "SELECT role FROM users WHERE user_id = ?", (target_user_id,)
        ).fetchone()
        if not target:
            raise ValueError("User not found.")
        if target["role"] == "admin" and new_role != "admin":
            admins = conn.execute(
                "SELECT COUNT(*) FROM users WHERE role = 'admin'"
            ).fetchone()[0]
            if admins <= 1:
                raise ValueError("You cannot remove the last admin.")
        conn.execute(
            "UPDATE users SET role = ? WHERE user_id = ?", (new_role, target_user_id)
        )
    log_event("role_changed", acting_user_id, "user", target_user_id, new_role)


def list_users(acting_user_id):
    """Admins only."""
    require_permission(acting_user_id, "manage_users")
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT user_id, username, email, full_name, role, created_at "
            "FROM users ORDER BY created_at DESC"
        )]


def get_login_records(acting_user_id, limit=50):
    """Admins only. Saved login and signup attempts, newest first."""
    require_permission(acting_user_id, "view_audit_log")
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT e.event_id, e.action, e.created_at, e.details, u.username, u.email "
            "FROM audit_events e LEFT JOIN users u ON u.user_id = e.user_id "
            "WHERE e.action IN ('register', 'login', 'login_failed') "
            "ORDER BY e.event_id DESC LIMIT ?",
            (limit,),
        )]


# -----------------------------------------------------
# Users and login
# -----------------------------------------------------
def register_user(username, email, password, full_name, municipality=None) -> int:
    """Create a user. Returns the new user_id. Raises ValueError on bad/duplicate input."""
    username, email = username.strip(), email.strip().lower()
    if not username or not email or not full_name.strip():
        raise ValueError("Username, email and full name are required.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO users (username, email, password_hash, full_name, municipality) "
                "VALUES (?, ?, ?, ?, ?)",
                (username, email, _hash_password(password), full_name.strip(), municipality),
            )
            user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        raise ValueError("Username or email is already taken.")
    log_event("register", user_id, "user", user_id)
    return user_id


def authenticate_user(username_or_email, password):
    """Return the user as a dict (no password hash) if the login is valid, else None."""
    ident = username_or_email.strip()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (ident, ident.lower()),
        ).fetchone()
    if row and _verify_password(password, row["password_hash"]):
        log_event("login", row["user_id"], "user", row["user_id"])
        user = dict(row)
        user.pop("password_hash")
        return user
    log_event("login_failed", row["user_id"] if row else None, details=f"identifier: {ident}")
    return None


def get_user(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT user_id, username, email, full_name, municipality, bio, role, created_at "
            "FROM users WHERE user_id = ?",
            (user_id,),
        ).fetchone()
    return dict(row) if row else None


# -----------------------------------------------------
# Sports and preferences
# -----------------------------------------------------
def list_sports():
    with get_connection() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM sports ORDER BY name")]


def set_sport_preference(user_id, sport_id, skill_level="beginner") -> None:
    """Add or update a sport the user plays."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO sports_preferences (user_id, sport_id, skill_level) VALUES (?, ?, ?) "
            "ON CONFLICT(user_id, sport_id) DO UPDATE SET skill_level = excluded.skill_level",
            (user_id, sport_id, skill_level),
        )


def get_user_sports(user_id):
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT s.sport_id, s.name, sp.skill_level FROM sports_preferences sp "
            "JOIN sports s ON s.sport_id = sp.sport_id WHERE sp.user_id = ? ORDER BY s.name",
            (user_id,),
        )]


# -----------------------------------------------------
# Venues and recommendations
# -----------------------------------------------------
def add_venue(name, added_by, sport_ids, address=None, municipality=None,
              latitude=None, longitude=None, venue_type=None) -> int:
    """Submit a venue (starts as 'pending' until an admin approves it)."""
    require_permission(added_by, "add_venue")
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO venues (name, address, municipality, latitude, longitude, "
            "venue_type, added_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (name, address, municipality, latitude, longitude, venue_type, added_by),
        )
        venue_id = cur.lastrowid
        conn.executemany(
            "INSERT OR IGNORE INTO venue_sports (venue_id, sport_id) VALUES (?, ?)",
            [(venue_id, sid) for sid in sport_ids],
        )
    log_event("venue_added", added_by, "venue", venue_id)
    return venue_id


def set_venue_status(venue_id, status, admin_id) -> None:
    """Approve or reject a venue ('approved' / 'rejected'). Admins only."""
    require_permission(admin_id, "approve_venue")
    if status not in ("pending", "approved", "rejected"):
        raise ValueError("Invalid venue status.")
    with get_connection() as conn:
        conn.execute("UPDATE venues SET status = ? WHERE venue_id = ?", (status, venue_id))
    log_event(f"venue_{status}", admin_id, "venue", venue_id)


def list_pending_venues(admin_id):
    """Admins only: venues waiting for approval."""
    require_permission(admin_id, "approve_venue")
    return list_venues(status="pending")


def list_venues(sport_id=None, municipality=None, status="approved"):
    """Venues with their sports and average rating. Filters are optional."""
    sql = (
        "SELECT v.*, "
        "  (SELECT GROUP_CONCAT(s.name, ', ') FROM venue_sports vs "
        "     JOIN sports s ON s.sport_id = vs.sport_id WHERE vs.venue_id = v.venue_id) AS sports, "
        "  (SELECT ROUND(AVG(rating), 1) FROM venue_recommendations r "
        "     WHERE r.venue_id = v.venue_id) AS avg_rating, "
        "  (SELECT COUNT(*) FROM venue_recommendations r "
        "     WHERE r.venue_id = v.venue_id) AS review_count "
        "FROM venues v WHERE v.status = ?"
    )
    params = [status]
    if sport_id:
        sql += " AND v.venue_id IN (SELECT venue_id FROM venue_sports WHERE sport_id = ?)"
        params.append(sport_id)
    if municipality:
        sql += " AND v.municipality = ?"
        params.append(municipality)
    sql += " ORDER BY v.name"
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql, params)]


def add_recommendation(venue_id, user_id, rating, comment=None) -> None:
    """Rate/review a venue. One review per user per venue (a new one replaces the old)."""
    require_permission(user_id, "add_review")
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO venue_recommendations (venue_id, user_id, rating, comment) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(venue_id, user_id) DO UPDATE SET "
            "rating = excluded.rating, comment = excluded.comment, "
            "created_at = datetime('now')",
            (venue_id, user_id, rating, comment),
        )


def get_recommendations(venue_id):
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT r.*, u.username FROM venue_recommendations r "
            "JOIN users u ON u.user_id = r.user_id WHERE r.venue_id = ? "
            "ORDER BY r.created_at DESC",
            (venue_id,),
        )]


# -----------------------------------------------------
# Partner posts
# -----------------------------------------------------
def create_partner_post(requester_id, sport_id, scheduled_at, venue_id=None,
                        skill_level_wanted="any", slots_needed=1, description=None) -> int:
    """scheduled_at format: 'YYYY-MM-DD HH:MM'."""
    require_permission(requester_id, "create_post")
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO partner_posts (requester_id, sport_id, venue_id, scheduled_at, "
            "skill_level_wanted, slots_needed, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (requester_id, sport_id, venue_id, scheduled_at,
             skill_level_wanted, slots_needed, description),
        )
        post_id = cur.lastrowid
    log_event("partner_post_created", requester_id, "partner_post", post_id)
    return post_id


def list_open_posts(sport_id=None):
    sql = (
        "SELECT p.*, s.name AS sport, u.username AS posted_by, v.name AS venue_name, "
        "  (SELECT COUNT(*) FROM partner_responses r "
        "     WHERE r.post_id = p.post_id AND r.status = 'accepted') AS accepted_count "
        "FROM partner_posts p "
        "JOIN sports s ON s.sport_id = p.sport_id "
        "JOIN users u ON u.user_id = p.requester_id "
        "LEFT JOIN venues v ON v.venue_id = p.venue_id "
        "WHERE p.status = 'open'"
    )
    params = []
    if sport_id:
        sql += " AND p.sport_id = ?"
        params.append(sport_id)
    sql += " ORDER BY p.scheduled_at"
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(sql, params)]


def join_partner_post(post_id, user_id) -> None:
    """Ask to join a post. Raises ValueError if it's your own post or already requested."""
    require_permission(user_id, "join_post")
    with get_connection() as conn:
        post = conn.execute(
            "SELECT requester_id, status FROM partner_posts WHERE post_id = ?", (post_id,)
        ).fetchone()
        if not post or post["status"] != "open":
            raise ValueError("This post is no longer open.")
        if post["requester_id"] == user_id:
            raise ValueError("You can't join your own post.")
        try:
            conn.execute(
                "INSERT INTO partner_responses (post_id, user_id) VALUES (?, ?)",
                (post_id, user_id),
            )
        except sqlite3.IntegrityError:
            raise ValueError("You already asked to join this post.")
    log_event("partner_join_requested", user_id, "partner_post", post_id)


def respond_to_join(response_id, accept: bool, owner_id) -> None:
    """Post owner accepts/declines. Marks the post 'full' once all slots are taken."""
    with get_connection() as conn:
        resp = conn.execute(
            "SELECT r.post_id, p.requester_id, p.slots_needed FROM partner_responses r "
            "JOIN partner_posts p ON p.post_id = r.post_id WHERE r.response_id = ?",
            (response_id,),
        ).fetchone()
        if not resp or resp["requester_id"] != owner_id:
            raise ValueError("Only the post owner can respond.")
        conn.execute(
            "UPDATE partner_responses SET status = ? WHERE response_id = ?",
            ("accepted" if accept else "declined", response_id),
        )
        accepted = conn.execute(
            "SELECT COUNT(*) FROM partner_responses WHERE post_id = ? AND status = 'accepted'",
            (resp["post_id"],),
        ).fetchone()[0]
        if accepted >= resp["slots_needed"]:
            conn.execute(
                "UPDATE partner_posts SET status = 'full' WHERE post_id = ?", (resp["post_id"],)
            )


# -----------------------------------------------------
# Dashboard
# -----------------------------------------------------
def get_dashboard_stats():
    with get_connection() as conn:
        one = lambda q: conn.execute(q).fetchone()[0]
        return {
            "total_users": one("SELECT COUNT(*) FROM users"),
            "approved_venues": one("SELECT COUNT(*) FROM venues WHERE status = 'approved'"),
            "open_posts": one("SELECT COUNT(*) FROM partner_posts WHERE status = 'open'"),
            "total_reviews": one("SELECT COUNT(*) FROM venue_recommendations"),
        }


if __name__ == "__main__":
    init_db()
    print("Database ready at:", DB_PATH)
    print("Stats:", get_dashboard_stats())
