
import flet as ft


def build():
    return ft.Column(
        controls=[
            ft.Text(
                "Sports Venues",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            ft.Text(
                "Explore sports facilities around Camarines Sur.",
                color="#AAB6C8",
            ),
            ft.Container(
                content=ft.Text(
                    "OpenStreetMap will be displayed here.",
                    color="#A3E635",
                ),
                bgcolor="#202D40",
                padding=20,
                border_radius=12,
            ),
        ],
        spacing=15,
    )
