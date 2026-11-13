
import flet as ft

from app import theme


def build():
    colors = theme.get_colors()

    return ft.Container(
        bgcolor=colors["BG"],
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text(
                    "My Profile",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=colors["WHITE"],
                ),

                ft.Text(
                    "Manage your sports preferences and information.",
                    color=colors["MUTED"],
                ),

                ft.Container(
                    content=ft.Text(
                        "User profile information will appear here.",
                        color=colors["GREEN"],
                    ),
                    bgcolor=colors["CARD"],
                    padding=20,
                    border_radius=12,
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
        ),
    )
