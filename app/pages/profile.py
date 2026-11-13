
import flet as ft


def build():
    return ft.Column(
        controls=[
            ft.Text(
                "My Profile",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            ft.Text(
                "Manage your sports preferences and information.",
                color="#AAB6C8",
            ),
            ft.Container(
                content=ft.Text(
                    "User profile information will appear here.",
                    color="#A3E635",
                ),
                bgcolor="#202D40",
                padding=20,
                border_radius=12,
            ),
        ],
        spacing=15,
    )
