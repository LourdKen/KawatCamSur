
import flet as ft
from app import theme


# =====================================
# STATISTIC CARDS
# =====================================

def stat_card(title, description, icon):
    colors = theme.get_colors()

    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4},
        padding=16,
        bgcolor=colors["CARD"],
        border=ft.Border.all(1, colors["BORDER"]),
        border_radius=14,
        content=ft.Row(
            controls=[
                ft.Container(
                    width=42,
                    height=42,
                    bgcolor=colors["ACTIVE_BG"],
                    border_radius=12,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(
                        icon,
                        color=colors["GREEN"],
                        size=22,
                    ),
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            title,
                            size=12,
                            color=colors["MUTED"],
                        ),
                        ft.Text(
                            description,
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=colors["WHITE"],
                        ),
                    ],
                    spacing=4,
                    expand=True,
                ),
            ],
            spacing=12,
        ),
    )


# =====================================
# SPORTS CARDS
# =====================================

def sports_card(name, icon):
    colors = theme.get_colors()

    return ft.Container(
        col={"xs": 12, "sm": 6, "md": 4},
        padding=16,
        bgcolor=colors["CARD"],
        border=ft.Border.all(1, colors["BORDER"]),
        border_radius=12,
        content=ft.Row(
            controls=[
                ft.Icon(
                    icon,
                    color=colors["GREEN"],
                    size=24,
                ),
                ft.Text(
                    name,
                    size=14,
                    color=colors["WHITE"],
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(expand=True),
                ft.Icon(
                    ft.Icons.ARROW_FORWARD_IOS,
                    color=colors["MUTED"],
                    size=14,
                ),
            ],
        ),
    )


# =====================================
# SECTION HEADERS
# =====================================

def section_header(title, subtitle=None):
    colors = theme.get_colors()

    controls = [
        ft.Text(
            title,
            size=19,
            weight=ft.FontWeight.BOLD,
            color=colors["WHITE"],
        )
    ]

    if subtitle:
        controls.append(
            ft.Text(
                subtitle,
                size=12,
                color=colors["MUTED"],
            )
        )

    return ft.Column(
        controls=controls,
        spacing=5,
    )


# =====================================
# DASHBOARD PAGE
# =====================================

def build():
    colors = theme.get_colors()

    return ft.Container(
        bgcolor=colors["BG"],
        expand=True,
        content=ft.Column(
            controls=[

                # HEADER
                ft.Column(
                    controls=[
                        ft.Text(
                            "Dashboard",
                            size=27,
                            weight=ft.FontWeight.BOLD,
                            color=colors["WHITE"],
                        ),
                        ft.Text(
                            "Welcome to your local sports community.",
                            size=13,
                            color=colors["MUTED"],
                        ),
                    ],
                    spacing=5,
                ),

                # STATISTICS
                ft.ResponsiveRow(
                    controls=[
                        stat_card(
                            "Sports Partners",
                            "Find Players",
                            ft.Icons.GROUP,
                        ),
                        stat_card(
                            "Sports Venues",
                            "Explore Places",
                            ft.Icons.LOCATION_ON,
                        ),
                        stat_card(
                            "Recommendations",
                            "Discover Places",
                            ft.Icons.RECOMMEND,
                        ),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),

                # HERO SECTION
                ft.Container(
                    padding=20,
                    bgcolor=colors["CARD"],
                    border=ft.Border.all(
                        1,
                        colors["BORDER"],
                    ),
                    border_radius=16,
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "YOUR SPORTS COMMUNITY",
                                size=10,
                                weight=ft.FontWeight.BOLD,
                                color=colors["GREEN"],
                            ),
                            ft.Text(
                                "Find your next game.",
                                size=25,
                                weight=ft.FontWeight.BOLD,
                                color=colors["WHITE"],
                            ),
                            ft.Text(
                                "Connect with fellow sports enthusiasts "
                                "and discover places to play throughout "
                                "Camarines Sur.",
                                size=13,
                                color=colors["MUTED"],
                            ),
                            ft.Container(
                                padding=ft.Padding.symmetric(
                                    horizontal=15,
                                    vertical=10,
                                ),
                                bgcolor=colors["GREEN"],
                                border_radius=9,
                                content=ft.Row(
                                    controls=[
                                        ft.Text(
                                            "Explore Sports",
                                            color=colors["BG"],
                                            weight=ft.FontWeight.BOLD,
                                            size=13,
                                        ),
                                        ft.Icon(
                                            ft.Icons.ARROW_FORWARD,
                                            color=colors["BG"],
                                            size=16,
                                        ),
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ),
                        ],
                        spacing=10,
                    ),
                ),

                # SPORTS SECTION
                section_header(
                    "Explore Sports",
                    "Choose your favorite sports and interests.",
                ),

                ft.ResponsiveRow(
                    controls=[
                        sports_card(
                            "Basketball",
                            ft.Icons.SPORTS_BASKETBALL,
                        ),
                        sports_card(
                            "Volleyball",
                            ft.Icons.SPORTS_VOLLEYBALL,
                        ),
                        sports_card(
                            "Badminton",
                            ft.Icons.SPORTS_TENNIS,
                        ),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),

                # LOCAL VENUES
                section_header(
                    "Discover Camarines Sur",
                    "Explore local sports facilities and locations.",
                ),

                ft.Container(
                    padding=18,
                    bgcolor=colors["CARD"],
                    border=ft.Border.all(
                        1,
                        colors["BORDER"],
                    ),
                    border_radius=14,
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.MAP_OUTLINED,
                                color=colors["GREEN"],
                                size=35,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "Explore Local Sports Venues",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["WHITE"],
                                    ),
                                    ft.Text(
                                        "Find places to play around "
                                        "Camarines Sur.",
                                        size=12,
                                        color=colors["MUTED"],
                                    ),
                                ],
                                spacing=5,
                                expand=True,
                            ),
                            ft.Icon(
                                ft.Icons.ARROW_FORWARD_IOS,
                                color=colors["MUTED"],
                                size=14,
                            ),
                        ],
                        spacing=12,
                    ),
                ),

                ft.Container(height=10),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
    )
