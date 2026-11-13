
import flet as ft

from app.pages import dashboard
from app.pages import partner_finder
from app.pages import venues
from app.pages import venue_recommendations
from app.pages import profile


def main(page: ft.Page):

    # PAGE SETTINGS
    page.title = "KawatCamSur"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#101827"
    page.padding = 0

    # Main content area
    content_area = ft.Container(
        expand=True,
        padding=30,
    )

    # Page navigation
    pages = {
        "Dashboard": dashboard.build,
        "Find Partners": partner_finder.build,
        "Sports Venues": venues.build,
        "Venue Recommendations": venue_recommendations.build,
        "My Profile": profile.build,
    }

    def navigate(page_name):
        content_area.content = pages[page_name]()
        page.update()

    # Sidebar buttons
    navigation_buttons = []

    for name in pages:
        navigation_buttons.append(
            ft.Button(
                content=ft.Text(name),
                on_click=lambda e, selected=name: navigate(selected),
            )
        )

    # SIDEBAR
    sidebar = ft.Container(
        width=240,
        bgcolor="#172235",
        padding=20,
        content=ft.Column(
            controls=[
                ft.Text(
                    "KawatCamSur",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#A3E635",
                ),

                ft.Text(
                    "SPORTS COMMUNITY",
                    size=11,
                    color="#AAB6C8",
                ),

                ft.Divider(color="#354258"),

                *navigation_buttons,
            ],
            spacing=15,
        ),
    )

    # Initial page
    content_area.content = dashboard.build()

    # MAIN LAYOUT
    page.add(
        ft.Row(
            controls=[
                sidebar,
                content_area,
            ],
            expand=True,
            spacing=0,
        )
    )


ft.run(main)
