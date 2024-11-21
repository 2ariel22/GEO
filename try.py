from Views.HojaVida import HojaVida
import flet as ft

def main(page: ft.Page):
    vista = HojaVida(page).getHojaVida()
    page.views.append(vista)
    page.update()


ft.app(target=main)