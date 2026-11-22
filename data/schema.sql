-- =====================================================
-- KawatCamSur Database Schema (SQLite)
-- Multi-Sport Partner Discovery and User-Generated
-- Venue Recommendation System
-- =====================================================
-- NOTE: run this on every connection from Python:
--   conn.execute("PRAGMA foreign_keys = ON;")
-- =====================================================

PRAGMA foreign_keys = ON;

-- -----------------------------------------------------
-- USERS
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    username       TEXT    NOT NULL UNIQUE,
    email          TEXT    NOT NULL UNIQUE,
    password_hash  TEXT    NOT NULL,              -- hashed, never plain text
    full_name      TEXT    NOT NULL,
    municipality   TEXT,
    bio            TEXT,
    role           TEXT    NOT NULL DEFAULT 'user'
                   CHECK (role IN ('user', 'admin')),
    created_at     TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- -----------------------------------------------------
-- SPORTS (lookup table)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS sports (
    sport_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    name      TEXT NOT NULL UNIQUE
);

-- -----------------------------------------------------
-- SPORTS_PREFERENCES (which sports a user plays, and how well)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS sports_preferences (
    user_id      INTEGER NOT NULL,
    sport_id     INTEGER NOT NULL,
    skill_level  TEXT    NOT NULL DEFAULT 'beginner'
                 CHECK (skill_level IN ('beginner', 'intermediate', 'advanced')),
    PRIMARY KEY (user_id, sport_id),
    FOREIGN KEY (user_id)  REFERENCES users(user_id)   ON DELETE CASCADE,
    FOREIGN KEY (sport_id) REFERENCES sports(sport_id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- VENUES (user-generated, optionally moderated)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS venues (
    venue_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    address       TEXT,
    municipality  TEXT,
    latitude      REAL CHECK (latitude  BETWEEN -90  AND 90),
    longitude     REAL CHECK (longitude BETWEEN -180 AND 180),
    venue_type    TEXT,                           -- e.g. court, field, gym, oval
    status        TEXT NOT NULL DEFAULT 'pending'
                  CHECK (status IN ('pending', 'approved', 'rejected')),
    added_by      INTEGER,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (added_by) REFERENCES users(user_id) ON DELETE SET NULL
);

-- -----------------------------------------------------
-- VENUE_SPORTS (which sports a venue supports)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS venue_sports (
    venue_id  INTEGER NOT NULL,
    sport_id  INTEGER NOT NULL,
    PRIMARY KEY (venue_id, sport_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE,
    FOREIGN KEY (sport_id) REFERENCES sports(sport_id) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- VENUE_RECOMMENDATIONS (ratings and reviews)
-- One review per user per venue.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS venue_recommendations (
    recommendation_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_id           INTEGER NOT NULL,
    user_id            INTEGER NOT NULL,
    rating             INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment            TEXT,
    created_at         TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (venue_id, user_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)  REFERENCES users(user_id)   ON DELETE CASCADE
);

-- -----------------------------------------------------
-- PARTNER_POSTS (a user looking for playmates)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS partner_posts (
    post_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    requester_id        INTEGER NOT NULL,
    sport_id            INTEGER NOT NULL,
    venue_id            INTEGER,
    scheduled_at        TEXT    NOT NULL,         -- 'YYYY-MM-DD HH:MM'
    skill_level_wanted  TEXT
                        CHECK (skill_level_wanted IN
                               ('beginner', 'intermediate', 'advanced', 'any')),
    slots_needed        INTEGER NOT NULL DEFAULT 1 CHECK (slots_needed >= 1),
    description         TEXT,
    status              TEXT NOT NULL DEFAULT 'open'
                        CHECK (status IN ('open', 'full', 'cancelled', 'completed')),
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (requester_id) REFERENCES users(user_id)   ON DELETE CASCADE,
    FOREIGN KEY (sport_id)     REFERENCES sports(sport_id),
    FOREIGN KEY (venue_id)     REFERENCES venues(venue_id) ON DELETE SET NULL
);

-- -----------------------------------------------------
-- PARTNER_RESPONSES (users joining a request)
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS partner_responses (
    response_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id   INTEGER NOT NULL,
    user_id      INTEGER NOT NULL,
    status       TEXT NOT NULL DEFAULT 'pending'
                 CHECK (status IN ('pending', 'accepted', 'declined')),
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE (post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES partner_posts(post_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)    REFERENCES users(user_id)               ON DELETE CASCADE
);

-- -----------------------------------------------------
-- INDEXES (speed up the common lookups)
-- -----------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_sports_preferences_sport    ON sports_preferences(sport_id);
CREATE INDEX IF NOT EXISTS idx_venues_status        ON venues(status);
CREATE INDEX IF NOT EXISTS idx_venues_municipality  ON venues(municipality);
CREATE INDEX IF NOT EXISTS idx_venue_sports_sport   ON venue_sports(sport_id);
CREATE INDEX IF NOT EXISTS idx_recs_venue           ON venue_recommendations(venue_id);
CREATE INDEX IF NOT EXISTS idx_posts_sport_stat  ON partner_posts(sport_id, status);
CREATE INDEX IF NOT EXISTS idx_posts_schedule    ON partner_posts(scheduled_at);
CREATE INDEX IF NOT EXISTS idx_responses_post    ON partner_responses(post_id);

-- -----------------------------------------------------
-- AUDIT_EVENTS (security / activity log)
-- user_id is kept as NULL if the user is later deleted,
-- so the history of what happened is preserved.
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_events (
    event_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER,
    action       TEXT NOT NULL,                  -- e.g. 'login', 'venue_added', 'venue_approved'
    entity_type  TEXT,                           -- e.g. 'venue', 'partner_post', 'user'
    entity_id    INTEGER,
    details      TEXT,
    created_at   TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_audit_user    ON audit_events(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_action  ON audit_events(action, created_at);
