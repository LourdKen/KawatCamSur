
import flet as ft


def build():
    return ft.Column(
        controls=[
            ft.Text(
                "Venue Recommendations",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            ft.Text(
                "Recommend a sports venue in Camarines Sur.",
                color="#AAB6C8",
            ),
            ft.Container(
                content=ft.Text(
                    "Venue submission form will appear here.",
                    color="#A3E635",
                ),
                bgcolor="#202D40",
                padding=20,
                border_radius=12,
            ),
        ],
        spacing=15,
    )
