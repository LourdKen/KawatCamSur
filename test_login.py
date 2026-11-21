import flet as ft
from app.pages import login

def main(page: ft.Page):
    page.title = "KawatCamSur - Login"
    page.bgcolor = "#0B1120"
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.add(login.build())

ft.run(main)