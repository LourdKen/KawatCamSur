import re
import secrets

import flet as ft
from database import register_user

# =====================================
# KAWATCAMSUR COLORS
# =====================================

BG = "#0B1120"
CARD = "#99182235"
INPUT_BG = "#55111C2F"
TEAL = "#14B8A6"
WHITE = "#F8FAFC"
MUTED = "#94A3B8"
BORDER = "#55FFFFFF"
ERROR = "#F87171"


def _make_username(email, attempt):
    """The form has no username field, so build one from the email.

    ana.cruz@mail.com -> ana.cruz (and ana.cruz4821 if that is already taken).
    """
    base = re.sub(r"[^a-z0-9_.]", "", email.split("@")[0].lower()) or "user"
    if attempt == 0:
        return base
    return f"{base}{secrets.randbelow(9000) + 1000}"


# =====================================
# SIGNUP PAGE
# =====================================

def build(on_login=None):
    """Signup screen.

    on_login - called after a successful signup and when "Login" is clicked,
               so the app can go back to the login screen.
    """

    # =================================
    # INPUT FIELDS
    # =================================

    full_name_field = ft.TextField(
        hint_text="Enter your full name",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        bgcolor=INPUT_BG,
        color=WHITE,
        border_color=BORDER,
        focused_border_color=TEAL,
        border_radius=9,
    )

    email_field = ft.TextField(
        hint_text="name@example.com",
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        keyboard_type=ft.KeyboardType.EMAIL,
        bgcolor=INPUT_BG,
        color=WHITE,
        border_color=BORDER,
        focused_border_color=TEAL,
        border_radius=9,
    )

    password_field = ft.TextField(
        hint_text="Create a password (min. 8 characters)",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        bgcolor=INPUT_BG,
        color=WHITE,
        border_color=BORDER,
        focused_border_color=TEAL,
        border_radius=9,
    )

    confirm_field = ft.TextField(
        hint_text="Confirm your password",
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        password=True,
        can_reveal_password=True,
        bgcolor=INPUT_BG,
        color=WHITE,
        border_color=BORDER,
        focused_border_color=TEAL,
        border_radius=9,
    )

    error_text = ft.Text(
        "",
        color=ERROR,
        size=12,
        visible=False,
        text_align=ft.TextAlign.CENTER,
    )

    # =================================
    # ACTIONS
    # =================================

    def show_error(message):
        error_text.value = message
        error_text.visible = True
        error_text.update()

    def do_signup(e):
        page = e.control.page

        full_name = (full_name_field.value or "").strip()
        email = (email_field.value or "").strip().lower()
        password = password_field.value or ""
        confirm = confirm_field.value or ""

        if not full_name or not email or not password:
            show_error("Please fill in all the fields.")
            return
        if "@" not in email or "." not in email.split("@")[-1]:
            show_error("Enter a valid email address.")
            return
        if password != confirm:
            show_error("Passwords do not match.")
            return

        # register_user() hashes the password, saves the user in the database
        # and writes a 'register' record in audit_events.
        created = False
        for attempt in range(5):
            try:
                register_user(
                    _make_username(email, attempt),
                    email,
                    password,
                    full_name,
                )
                created = True
                break
            except ValueError as err:
                if "already taken" not in str(err):
                    show_error(str(err))  # e.g. password too short
                    return
                # username or email taken: try another username

        if not created:
            show_error("An account with this email may already exist. Try logging in.")
            return

        error_text.visible = False
        error_text.update()

        page.show_dialog(
            ft.SnackBar(
                content=ft.Text("Account created! You can log in now.")
            )
        )

        if on_login:
            on_login(e)

    confirm_field.on_submit = do_signup

    # =================================
    # GLASS SIGNUP CARD
    # =================================

    signup_card = ft.Container(
        width=430,
        padding=30,
        bgcolor=CARD,
        border=ft.Border.all(1, BORDER),
        border_radius=22,
        content=ft.Column(
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[

                # BRAND
                ft.Column(
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            ft.Icons.SPORTS,
                            color=TEAL,
                            size=38,
                        ),
                        ft.Text(
                            "KawatCamSur",
                            size=27,
                            weight=ft.FontWeight.BOLD,
                            color=TEAL,
                        ),
                        ft.Text(
                            "FIND YOUR GAME. FIND YOUR PEOPLE.",
                            size=10,
                            color=MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),

                ft.Divider(color="#44FFFFFF"),

                # CREATE ACCOUNT
                ft.Column(
                    spacing=6,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text(
                            "Create Account",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=WHITE,
                        ),
                        ft.Text(
                            "Join the KawatCamSur sports community.",
                            size=12,
                            color=MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                    ],
                ),

                # FULL NAME
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            "Full Name",
                            color=WHITE,
                            size=13,
                        ),
                        full_name_field,
                    ],
                ),

                # EMAIL
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            "Email Address",
                            color=WHITE,
                            size=13,
                        ),
                        email_field,
                    ],
                ),

                # PASSWORD
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            "Password",
                            color=WHITE,
                            size=13,
                        ),
                        password_field,
                    ],
                ),

                # CONFIRM PASSWORD
                ft.Column(
                    spacing=6,
                    controls=[
                        ft.Text(
                            "Confirm Password",
                            color=WHITE,
                            size=13,
                        ),
                        confirm_field,
                    ],
                ),

                # ERROR MESSAGE (hidden until something is wrong)
                error_text,

                # CREATE ACCOUNT BUTTON
                ft.Button(
                    "Create Account",
                    height=48,
                    width=float("inf"),
                    bgcolor=TEAL,
                    color=WHITE,
                    on_click=do_signup,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(
                            radius=10,
                        ),
                    ),
                ),

                # LOGIN NAVIGATION
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=4,
                    controls=[
                        ft.Text(
                            "Already have an account?",
                            color=MUTED,
                            size=12,
                        ),
                        ft.TextButton(
                            "Login",
                            style=ft.ButtonStyle(
                                color=TEAL,
                            ),
                            on_click=on_login,
                        ),
                    ],
                ),
            ],
        ),
    )

    # =================================
    # FULL SCREEN SPORTS BACKGROUND
    # =================================

    return ft.Container(
        expand=True,
        bgcolor=BG,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        content=ft.Stack(
            expand=True,
            controls=[

                # BACKGROUND IMAGE
                ft.Image(
                    src="sports_hero.jpg",
                    fit=ft.BoxFit.COVER,
                    width=float("inf"),
                    height=float("inf"),
                ),

                # DARK OVERLAY AND GLASS CARD
                ft.Container(
                    expand=True,
                    bgcolor="#66071120",
                    padding=20,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            signup_card,
                        ],
                    ),
                ),
            ],
        ),
    )
