import flet as ft
from Views.Controls.RegisterView import RegisterView
from Resource.ApiLogin import ApiLogin  # Se usa la API interna para login
from Views.HojaVida import HojaVida

class Inicio:
    def __init__(self, page: ft.Page):
        self.page = page
        self.registroView = RegisterView(page)
        self.api = ApiLogin()  # Instancia de ApiLogin para verificar el login
        self.equipoView = HojaVida(page)

    def validar_usuario(self):
        # Obtén los valores ingresados por el usuario
        usuario = self.username.value
        contrasena = self.password.value

        # Usa la API para verificar si el usuario está registrado
        resultado = self.api.consultar_usuario(usuario, contrasena)

        # Devuelve el resultado de la validación
        return resultado

    def iniciarSesion(self, e):
        resultado = self.validar_usuario()

        # Muestra un SnackBar según el resultado
        if resultado["success"]:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Inicio de sesión exitoso"),
                action="OK",
            )
            self.page.views.append(self.equipoView.getHojaVida())
            
            # Aquí puedes redirigir a otra vista en caso de éxito
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Error: {resultado['message']}"),
                action="OK",
            )
        self.page.snack_bar.open = True
        self.page.update()

    def register(self, e):
        vista = self.registroView.getRegisterView()
        self.page.views.append(vista)
        self.page.update()

    def getInicioView(self):
        title = ft.Text(
            value="Bienvenidos a GEO",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        # Logo with Border Radius
        logo = ft.Container(
            content=ft.Image(
                src="https://i.postimg.cc/MKk6cMYW/logo.jpg",
                width=100,
                height=100,
                fit=ft.ImageFit.CONTAIN,
            ),
            border_radius=ft.BorderRadius(10, 10, 10, 10),  # Added border radius
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # Ensures the border radius is applied
        )

        # Row for title and logo
        title_with_logo = ft.Row(
            controls=[title, logo],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        
        about = ft.Text(
            value=(
                "Somos una compañía especializada en venta, mantenimiento y alquiler de "
                "equipos Médicos con profesionales altamente capacitados que brindan el soporte "
                "adecuado a las necesidades de las entidades de salud en Colombia."
            ),
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            weight=ft.FontWeight.W_200,
            size=20,
        )

        # Campos de entrada para login
        self.username = ft.TextField(
            label="Usuario",
            helper_text="Ingrese su usuario",
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )
        self.password = ft.TextField(
            label="Contraseña",
            helper_text="Ingrese su contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )

        login_button = ft.ElevatedButton(
            text="Iniciar Sesión",
            on_click=self.iniciarSesion,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10,
            ),
        )

        register_button = ft.ElevatedButton(
            text="Registrarte",
            on_click=self.register,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10,
            ),
        )

        contente = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                title_with_logo,  # Replace individual title and logo with this row
                ft.Container(padding=10),
                about,
                ft.Container(padding=10),
                self.username,
                ft.Container(padding=10),
                self.password,
                ft.Container(padding=10),
                ft.Row(
                    controls=[
                        login_button,
                        ft.Container(padding=2.5),
                        register_button,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            width=300,
        )

        login = ft.Row(
            controls=[
                ft.Container(content=contente, padding=20),
            ]
        )

        background = ft.Container(
            width=self.page.width,
            height=(1 * self.page.height),
            bgcolor="#efefef",
            alignment=ft.alignment.center,
            padding=0,
            margin=0,
        )

        contenido = ft.Row(
            controls=[login],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.View(
            route="/Inicio",
            controls=[
                ft.Stack(
                    [background, contenido],
                    width=self.page.width,
                    alignment=ft.alignment.center,
                ),
            ],
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )