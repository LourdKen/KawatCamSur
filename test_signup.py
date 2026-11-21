
import flet as ft
from app.pages import signup

def main(page: ft.Page):
    page.title = "KawatCamSur - Signup"
    page.bgcolor = "#0B1120"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.add(signup.build())

ft.run(main)
