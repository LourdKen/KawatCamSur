import flet as ft
from database import authenticate_user

def build():
    identifier = ft.TextField(label="Username or email")
    password = ft.TextField(label="Password", password=True, can_reveal_password=True)
    message = ft.Text(color="#F87171")

    def on_login(e):
        user = authenticate_user(identifier.value or "", password.value or "")
        if user:
            message.value = ""
            # success: store `user` and go to the dashboard here
        else:
            message.value = "Invalid username/email or password."
        message.update()

    return ft.Column([identifier, password, message,
                      ft.ElevatedButton("Log in", on_click=on_login)])

def get_login_records(limit=50):
    """Most recent login attempts, newest first."""
    with get_connection() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT e.event_id, e.action, e.created_at, e.details, u.username "
            "FROM audit_events e LEFT JOIN users u ON u.user_id = e.user_id "
            "WHERE e.action IN ('login', 'login_failed') "
            "ORDER BY e.event_id DESC LIMIT ?", (limit,)
        )]