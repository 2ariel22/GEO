import requests  # Reemplazamos aiohttp por requests
import json
import flet as ft


from Views.HojaVida import HojaVida

class Login():
    def __init__(self, page: ft.Page):
        self.page = page
        self.username = ft.TextField(
            value="awuiel",
            label="Usuario",
            helper_text="Ingrese su nombre de usuario",
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )

        # Campo de contraseña
        self.password = ft.TextField(
            value="2486",
            label="Contraseña",
            helper_text="Ingrese su contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )
        self.hojaVida = HojaVida(page)
        
      

   

    def peticion(self):
        payload = {
            "user": self.username.value,  # Obtén el valor del campo de usuario
            "pass": self.password.value   # Obtén el valor del campo de contraseña
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post("http://localhost:8080/login/valid", data=json.dumps(payload), headers=headers)
            return response.json()
        except Exception as e:
            # Error en la conexión o petición
            print(f"Error en la petición: {e}")
            return False

   

    def iniciarSesion(self, e):
        mensaje = self.peticion()
        #self.equipoView = Equipo(self.page)
        print(mensaje)
        if mensaje:  # Aquí puedes validar si el login fue exitoso según la respuesta
            print("Login exitoso:", mensaje)
            vista = self.hojaVida.getHojaVida()
            self.page.views.append(vista)
            self.page.update()
        else:
            print("Error en el login:", mensaje)
    def back(self, e):
        self.page.views.pop()
        self.page.update()
    def getInicioView(self):
        title = ft.Text(
            value="Iniciar Sesión",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            on_click=self.iniciarSesion,  # Ahora es completamente síncrono
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10
            ),
        )
        
        backButton = ft.ElevatedButton(
            text="<--",
            on_click=self.back,
        
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10
                
            ),
        )
       

        # Contenedor principal centrado
        contente = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                title,
                ft.Container(padding=10),
                self.username,
                ft.Container(padding=10),
                self.password,
                ft.Container(padding=5),
                ft.Row(controls=[
                    login_button,
                   ft.Container(padding=5),
                   backButton
                    
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER)
            ],
            width=300,
        )
        
        login = ft.Row(controls=[
            ft.Container(content=contente, padding=20)
        ])

        background = ft.Container(
            width=self.page.width,
            height=(1*self.page.height),
            bgcolor='#efefef',
            alignment=ft.alignment.center,
            padding=0,
            margin=0
        )

        contenido = ft.Row(controls=[login], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        # Contenedor resaltado en el centro
        return ft.View(
            route="/Login",
            controls=[
                ft.Stack(
                    [background, contenido],
                    width=self.page.width,
                    alignment=ft.alignment.center
                )
            ],
            padding=0,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
