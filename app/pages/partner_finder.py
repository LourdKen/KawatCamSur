
import flet as ft


def build():
    return ft.Column(
        controls=[
            ft.Text(
                "Find Sports Partners",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            ft.Text(
                "Discover players with similar sports interests.",
                color="#AAB6C8",
            ),
            ft.Container(
                content=ft.Text(
                    "Content-Based Filtering recommendations "
                    "will appear here.",
                    color="#A3E635",
                ),
                bgcolor="#202D40",
                padding=20,
                border_radius=12,
            ),
        ],
        spacing=15,
    )
