
import flet as ft

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


# =====================================
# SIGNUP PAGE
# =====================================

def build(on_login=None):

    def show_message(e):
        e.control.page.open(
            ft.SnackBar(
                content=ft.Text(
                    "Account registration will be connected later."
                )
            )
        )

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
                        ft.TextField(
                            hint_text="Enter your full name",
                            prefix_icon=ft.Icons.PERSON_OUTLINE,
                            bgcolor=INPUT_BG,
                            color=WHITE,
                            border_color=BORDER,
                            focused_border_color=TEAL,
                            border_radius=9,
                        ),
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
                        ft.TextField(
                            hint_text="name@example.com",
                            prefix_icon=ft.Icons.EMAIL_OUTLINED,
                            keyboard_type=ft.KeyboardType.EMAIL,
                            bgcolor=INPUT_BG,
                            color=WHITE,
                            border_color=BORDER,
                            focused_border_color=TEAL,
                            border_radius=9,
                        ),
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
                        ft.TextField(
                            hint_text="Create a password",
                            prefix_icon=ft.Icons.LOCK_OUTLINE,
                            password=True,
                            can_reveal_password=True,
                            bgcolor=INPUT_BG,
                            color=WHITE,
                            border_color=BORDER,
                            focused_border_color=TEAL,
                            border_radius=9,
                        ),
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
                        ft.TextField(
                            hint_text="Confirm your password",
                            prefix_icon=ft.Icons.LOCK_OUTLINE,
                            password=True,
                            can_reveal_password=True,
                            bgcolor=INPUT_BG,
                            color=WHITE,
                            border_color=BORDER,
                            focused_border_color=TEAL,
                            border_radius=9,
                        ),
                    ],
                ),

                # CREATE ACCOUNT BUTTON
                ft.Button(
                    "Create Account",
                    height=48,
                    width=float("inf"),
                    bgcolor=TEAL,
                    color=WHITE,
                    on_click=show_message,
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
