
import flet as ft

from app.pages import dashboard
from app.pages import partner_finder
from app.pages import venues
from app.pages import venue_recommendations
from app.pages import profile
from app import theme


MOBILE_BREAKPOINT = 700


def main(page: ft.Page):

    page.title = "KawatCamSur"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = theme.get_colors()["BG"]

    pages = {
        "Dashboard": dashboard.build,
        "Find Partners": partner_finder.build,
        "Sports Venues": venues.build,
        "Recommendations": venue_recommendations.build,
        "Profile": profile.build,
    }

    page_icons = {
        "Dashboard": ft.Icons.DASHBOARD_OUTLINED,
        "Find Partners": ft.Icons.GROUP_OUTLINED,
        "Sports Venues": ft.Icons.MAP_OUTLINED,
        "Recommendations": ft.Icons.RECOMMEND,
        "Profile": ft.Icons.PERSON_OUTLINE,
    }

    current_page = "Dashboard"

    # =====================================
    # MAIN CONTENT AREA
    # =====================================

    content_area = ft.Container(
        expand=True,
        padding=20,
    )

    # =====================================
    # THEME TOGGLE
    # =====================================

    def toggle_theme(e):

        new_theme = (
            "light"
            if theme.current_theme == "dark"
            else "dark"
        )

        theme.set_theme(new_theme)

        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if new_theme == "light"
            else ft.ThemeMode.DARK
        )

        page.bgcolor = theme.get_colors()["BG"]

        refresh_page()

    # =====================================
    # PAGE HEADER
    # =====================================

    def build_page_content(name):

        colors = theme.get_colors()

        theme_button = ft.IconButton(
            icon=(
                ft.Icons.LIGHT_MODE
                if theme.current_theme == "dark"
                else ft.Icons.DARK_MODE
            ),
            icon_color=colors["GREEN"],
            icon_size=24,
            tooltip="Switch Light/Dark Mode",
            on_click=toggle_theme,
        )

        return ft.Container(
            expand=True,
            bgcolor=colors["BG"],
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(expand=True),
                            theme_button,
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),

                    ft.Container(
                        expand=True,
                        content=pages[name](),
                    ),
                ],
                spacing=5,
                expand=True,
            ),
        )

    # =====================================
    # DESKTOP SIDEBAR
    # =====================================

    def make_sidebar_item(name):

        colors = theme.get_colors()
        active = name == current_page

        return ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=14,
                vertical=13,
            ),
            border_radius=10,
            bgcolor=(
                colors["ACTIVE_BG"]
                if active else None
            ),
            on_click=lambda e: navigate(name),

            content=ft.Row(
                controls=[
                    ft.Icon(
                        page_icons[name],
                        color=(
                            colors["GREEN"]
                            if active else colors["MUTED"]
                        ),
                        size=20,
                    ),

                    ft.Text(
                        name,
                        color=(
                            colors["WHITE"]
                            if active else colors["MUTED"]
                        ),
                        size=14,
                        weight=(
                            ft.FontWeight.BOLD
                            if active else None
                        ),
                    ),
                ],
                spacing=12,
            ),
        )

    sidebar = ft.Container(
        width=255,
        padding=20,

    )

    # =====================================
    # MOBILE BOTTOM NAVIGATION
    # =====================================

    def make_mobile_item(name):

        colors = theme.get_colors()
        active = name == current_page

        return ft.Container(
            expand=True,
            padding=ft.Padding.symmetric(
                vertical=8,
                horizontal=2,
            ),
            alignment=ft.Alignment.CENTER,
            bgcolor=(
                colors["ACTIVE_BG"]
                if active else None
            ),
            border_radius=10,
            on_click=lambda e: navigate(name),

            content=ft.Column(
                controls=[
                    ft.Icon(
                        page_icons[name],
                        color=(
                            colors["GREEN"]
                            if active else colors["MUTED"]
                        ),
                        size=20,
                    ),

                    ft.Text(
                        name,
                        size=9,
                        color=(
                            colors["WHITE"]
                            if active else colors["MUTED"]
                        ),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),
                spacing=4,
            ),
        )

    mobile_nav = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=5,
            vertical=5,
        ),
    )

    # =====================================
    # REFRESH SIDEBAR AND MOBILE NAVIGATION
    # =====================================

    def update_navigation():

        colors = theme.get_colors()

        sidebar.bgcolor = colors["SIDEBAR"]

        sidebar.content = ft.Column(
            controls=[
                ft.Text(
                    "KawatCamSur",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=colors["GREEN"],
                ),

                ft.Text(
                    "YOUR LOCAL SPORTS COMMUNITY",
                    size=9,
                    color=colors["MUTED"],
                ),

                ft.Divider(
                    color=colors["BORDER"],
                    height=30,
                ),

                ft.Text(
                    "MENU",
                    size=11,
                    color=colors["MUTED"],
                ),

                *[
                    make_sidebar_item(name)
                    for name in pages
                ],

                ft.Container(expand=True),

                ft.Divider(color=colors["BORDER"]),

                ft.Text(
                    "Camarines Sur, PH",
                    size=12,
                    color=colors["MUTED"],
                ),
            ],
            spacing=10,
            expand=True,
        )

        mobile_nav.bgcolor = colors["SIDEBAR"]
        mobile_nav.border = ft.Border.only(
            top=ft.BorderSide(1, colors["BORDER"])
        )

        mobile_nav.content = ft.Row(
            controls=[
                make_mobile_item(name)
                for name in pages
            ],
            spacing=2,
        )

    # =====================================
    # NAVIGATION
    # =====================================

    def refresh_page():

        colors = theme.get_colors()

        content_area.bgcolor = colors["BG"]
        content_area.content = build_page_content(
            current_page
        )

        update_navigation()

        page.update()

    def navigate(name):

        nonlocal current_page

        current_page = name

        refresh_page()

    # =====================================
    # RESPONSIVE LAYOUT
    # =====================================

    main_row = ft.Row(
        controls=[
            sidebar,
            content_area,
        ],
        spacing=0,
        expand=True,
    )

    root = ft.Column(
        controls=[
            main_row,
            mobile_nav,
        ],
        spacing=0,
        expand=True,
    )

    def update_layout(e=None):

        is_mobile = (
            (page.width or 800) < MOBILE_BREAKPOINT
        )

        sidebar.visible = not is_mobile
        mobile_nav.visible = is_mobile

        page.update()

    page.on_resize = update_layout

    # =====================================
    # START APPLICATION
    # =====================================

    update_navigation()
    refresh_page()

    page.add(root)

    update_layout()


ft.run(main)
