
import flet as ft
from app import theme


def build():
    colors = theme.get_colors()

    return ft.Container(
        bgcolor=colors["BG"],
        expand=True,
        content=ft.Column(
            controls=[

                # PAGE TITLE
                ft.Text(
                    "Venue Recommendations",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=colors["WHITE"],
                ),

                # DESCRIPTION
                ft.Text(
                    "Recommend a sports venue in Camarines Sur.",
                    size=14,
                    color=colors["MUTED"],
                ),

                # SUBMISSION PLACEHOLDER
                ft.Container(
                    padding=20,
                    bgcolor=colors["CARD"],
                    border=ft.Border.all(
                        1,
                        colors["BORDER"],
                    ),
                    border_radius=12,
                    content=ft.Text(
                        "Venue submission form will appear here.",
                        color=colors["GREEN"],
                        size=14,
                    ),
                ),

            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )
