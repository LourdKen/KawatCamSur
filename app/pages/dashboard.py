
import flet as ft


def build():
    return ft.Column(
        controls=[
            ft.Text(
                "Dashboard",
                size=30,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),
            ft.Text(
                "Welcome to your local sports community.",
                size=15,
                color="#AAB6C8",
            ),

            ft.Container(height=10),

            # Overview cards
            ft.Row(
                controls=[
                    overview_card("Sports Partners", "Find players"),
                    overview_card("Sports Venues", "Explore places"),
                    overview_card("Recommendations", "Share a venue"),
                ],
                spacing=15,
                wrap=True,
            ),

            ft.Container(height=20),

            ft.Text(
                "Explore KawatCamSur",
                size=22,
                weight=ft.FontWeight.BOLD,
                color="#FFFFFF",
            ),

            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Find your next sports partner!",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color="#A3E635",
                        ),
                        ft.Text(
                            "Connect with people who share your "
                            "favorite sports across Camarines Sur.",
                            color="#D1D5DB",
                            size=14,
                        ),
                    ],
                    spacing=10,
                ),
                bgcolor="#202D40",
                padding=25,
                border_radius=12,
            ),
        ],
        spacing=12,
    )


def overview_card(title, description):
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color="#A3E635",
                ),
                ft.Text(
                    description,
                    size=13,
                    color="#D1D5DB",
                ),
            ],
            spacing=8,
        ),
        bgcolor="#202D40",
        padding=20,
        border_radius=12,
        width=200,
    )
