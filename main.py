
import asyncio
import flet as ft

from app import theme
from app.pages import (
    dashboard,
    partner_finder,
    venues,
    venue_recommendations,
    profile,
    login,
    signup,
)


# ==================================================
# APP CONFIGURATION
# ==================================================

APP_NAME = "KawatCamSur"
MOBILE_BREAKPOINT = 700

DARK_BG = "#0B1120"
GREEN = "#84CC16"
TEAL = "#14B8A6"


# ==================================================
# APPLICATION PAGES
# ==================================================

PAGES = {
    "Dashboard": dashboard.build,
    "Find Partners": partner_finder.build,
    "Sports Venues": venues.build,
    "Recommendations": venue_recommendations.build,
    "Profile": profile.build,
}

PAGE_ICONS = {
    "Dashboard": ft.Icons.DASHBOARD_OUTLINED,
    "Find Partners": ft.Icons.GROUP_OUTLINED,
    "Sports Venues": ft.Icons.MAP_OUTLINED,
    "Recommendations": ft.Icons.RECOMMEND,
    "Profile": ft.Icons.PERSON_OUTLINE,
}


# ==================================================
# MAIN APPLICATION
# ==================================================

def main(page: ft.Page):

    # ----------------------------------------------
    # INITIAL SETTINGS
    # ----------------------------------------------

    page.title = APP_NAME
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0
    page.bgcolor = DARK_BG

    current_page = "Dashboard"
    app_started = False
    animation_running = False

    # ----------------------------------------------
    # SUBTLE BACKGROUND LIGHTING
    # ----------------------------------------------

    green_glow = ft.Container(
        width=520,
        height=520,
        border_radius=260,
        gradient=ft.RadialGradient(
            colors=[
                "#3384CC16",
                "#1884CC16",
                "#0084CC16",
            ],
        ),
        offset=ft.Offset(-0.35, -0.35),
        animate_offset=ft.Animation(
            9000,
            ft.AnimationCurve.EASE_IN_OUT,
        ),
        opacity=0.8,
    )

    teal_glow = ft.Container(
        width=560,
        height=560,
        border_radius=280,
        gradient=ft.RadialGradient(
            colors=[
                "#3314B8A6",
                "#1814B8A6",
                "#0014B8A6",
            ],
        ),
        offset=ft.Offset(0.45, 0.35),
        animate_offset=ft.Animation(
            11000,
            ft.AnimationCurve.EASE_IN_OUT,
        ),
        opacity=0.7,
    )

    background_layer = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=[
                "#0B1120",
                "#101B2D",
                "#0B1120",
            ],
        ),
        content=ft.Stack(
            controls=[
                green_glow,
                teal_glow,
            ],
        ),
    )

    # ----------------------------------------------
    # BACKGROUND ANIMATION
    # ----------------------------------------------

    async def animate_background():

        nonlocal animation_running

        if animation_running:
            return

        animation_running = True

        try:
            while app_started:

                if theme.current_theme == "dark":

                    green_glow.offset = ft.Offset(
                        0.25, 0.15
                    )

                    teal_glow.offset = ft.Offset(
                        -0.25, -0.15
                    )

                else:

                    green_glow.offset = ft.Offset(
                        -0.35, -0.35
                    )

                    teal_glow.offset = ft.Offset(
                        0.45, 0.35
                    )

                page.update()

                await asyncio.sleep(9)

                if theme.current_theme == "dark":

                    green_glow.offset = ft.Offset(
                        -0.35, -0.35
                    )

                    teal_glow.offset = ft.Offset(
                        0.45, 0.35
                    )

                page.update()

                await asyncio.sleep(9)

        except Exception as error:
            print("Background animation:", error)

        finally:
            animation_running = False

    # ----------------------------------------------
    # MAIN UI CONTAINERS
    # ----------------------------------------------

    content_area = ft.Container(
        expand=True,
        padding=20,
        bgcolor="#00000000",
    )

    sidebar = ft.Container(
        width=255,
        padding=20,
    )

    mobile_nav = ft.Container(
        padding=ft.Padding.symmetric(
            horizontal=5,
            vertical=5,
        ),
    )

    # ----------------------------------------------
    # THEME MANAGEMENT
    # ----------------------------------------------

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

        page.bgcolor = (
            "#F1F5F9"
            if new_theme == "light"
            else DARK_BG
        )

        background_layer.gradient = (
            ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[
                    "#F1F5F9",
                    "#E2E8F0",
                    "#F8FAFC",
                ],
            )
            if new_theme == "light"
            else ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment.BOTTOM_RIGHT,
                colors=[
                    "#0B1120",
                    "#101B2D",
                    "#0B1120",
                ],
            )
        )

        refresh_page()

    # ----------------------------------------------
    # PAGE HEADER AND CONTENT
    # ----------------------------------------------

    def build_page_content(name):

        colors = theme.get_colors()

        theme_button = ft.IconButton(
            icon=(
                ft.Icons.LIGHT_MODE
                if theme.current_theme == "dark"
                else ft.Icons.DARK_MODE
            ),
            icon_color=colors["GREEN"],
            icon_size=23,
            tooltip="Switch Light/Dark Mode",
            on_click=toggle_theme,
        )

        return ft.Container(
            expand=True,
            bgcolor="#00000000",
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
                        content=PAGES[name](),
                    ),
                ],
                spacing=5,
                expand=True,
            ),
        )

    # ----------------------------------------------
    # DESKTOP SIDEBAR
    # ----------------------------------------------

    def make_sidebar_item(name):

        colors = theme.get_colors()
        active = name == current_page

        return ft.Container(
            padding=ft.Padding.symmetric(
                horizontal=14,
                vertical=13,
            ),
            border_radius=12,
            bgcolor=(
                colors["ACTIVE_BG"]
                if active else None
            ),
            on_click=lambda e: navigate(name),
            ink=True,
            content=ft.Row(
                controls=[
                    ft.Icon(
                        PAGE_ICONS[name],
                        color=(
                            colors["GREEN"]
                            if active
                            else colors["MUTED"]
                        ),
                        size=20,
                    ),
                    ft.Text(
                        name,
                        color=(
                            colors["WHITE"]
                            if active
                            else colors["MUTED"]
                        ),
                        size=14,
                        weight=(
                            ft.FontWeight.BOLD
                            if active
                            else None
                        ),
                    ),
                ],
                spacing=12,
            ),
        )

    def update_sidebar():

        colors = theme.get_colors()

        sidebar.bgcolor = colors["SIDEBAR"]

        sidebar.content = ft.Column(
            controls=[
                ft.Container(
                    padding=ft.Padding.only(
                        top=8,
                        bottom=8,
                    ),
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                APP_NAME,
                                size=23,
                                weight=ft.FontWeight.BOLD,
                                color=colors["GREEN"],
                            ),
                            ft.Text(
                                "SPORTS COMMUNITY",
                                size=9,
                                color=colors["MUTED"],
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=4,
                    ),
                ),

                ft.Divider(
                    color=colors["BORDER"],
                    height=25,
                ),

                ft.Text(
                    "MENU",
                    size=10,
                    color=colors["MUTED"],
                    weight=ft.FontWeight.BOLD,
                ),

                *[
                    make_sidebar_item(name)
                    for name in PAGES
                ],

                ft.Container(expand=True),

                ft.Divider(
                    color=colors["BORDER"],
                ),

                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.LOCATION_ON_OUTLINED,
                            color=colors["GREEN"],
                            size=17,
                        ),
                        ft.Text(
                            "Camarines Sur, PH",
                            size=12,
                            color=colors["MUTED"],
                        ),
                    ],
                    spacing=8,
                ),
            ],
            spacing=10,
            expand=True,
        )

    # ----------------------------------------------
    # MOBILE BOTTOM NAVIGATION
    # ----------------------------------------------

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
                        PAGE_ICONS[name],
                        color=(
                            colors["GREEN"]
                            if active
                            else colors["MUTED"]
                        ),
                        size=20,
                    ),
                    ft.Text(
                        name,
                        size=9,
                        color=(
                            colors["WHITE"]
                            if active
                            else colors["MUTED"]
                        ),
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
        )

    def update_mobile_navigation():

        colors = theme.get_colors()

        mobile_nav.bgcolor = colors["SIDEBAR"]

        mobile_nav.border = ft.Border.only(
            top=ft.BorderSide(
                1,
                colors["BORDER"],
            )
        )

        mobile_nav.content = ft.Row(
            controls=[
                make_mobile_item(name)
                for name in PAGES
            ],
            spacing=2,
        )

    # ----------------------------------------------
    # NAVIGATION REFRESH
    # ----------------------------------------------

    def update_navigation():

        update_sidebar()
        update_mobile_navigation()

    def refresh_page():

        content_area.content = build_page_content(
            current_page
        )

        update_navigation()

        page.update()

    def navigate(name):

        nonlocal current_page

        if name not in PAGES:
            return

        current_page = name

        refresh_page()

    # ----------------------------------------------
    # RESPONSIVE LAYOUT
    # ----------------------------------------------

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

        if not app_started:
            return

        is_mobile = (
            (page.width or 800) < MOBILE_BREAKPOINT
        )

        sidebar.visible = not is_mobile
        mobile_nav.visible = is_mobile

        page.update()

    # ----------------------------------------------
    # LOGIN AND SIGNUP SCREENS
    # ----------------------------------------------

    def show_login(e=None):

        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = DARK_BG
        page.padding = 0

        page.clean()

        page.add(
            login.build(
                on_signup=show_signup
            )
        )

        page.update()

    def show_signup(e=None):

        page.theme_mode = ft.ThemeMode.DARK
        page.bgcolor = DARK_BG
        page.padding = 0

        page.clean()

        page.add(
            signup.build(
                on_login=show_login
            )
        )

        page.update()

    # ----------------------------------------------
    # OPEN MAIN APPLICATION
    # ----------------------------------------------

    def show_app():

        nonlocal app_started

        app_started = True

        page.padding = 0
        page.spacing = 0
        page.bgcolor = DARK_BG

        page.clean()

        page.add(
            ft.Stack(
                controls=[
                    background_layer,
                    root,
                ],
                expand=True,
            )
        )

        update_navigation()
        refresh_page()
        update_layout()

        page.run_task(animate_background)

    # ----------------------------------------------
    # APPLICATION STARTUP
    # ----------------------------------------------

    page.on_resize = update_layout

    # Keep the current startup behavior
    show_app()


# ==================================================
# RUN APPLICATION
# ==================================================

ft.run(
    main,
    assets_dir="assets",
)
