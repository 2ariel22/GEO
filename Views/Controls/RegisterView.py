import flet as ft
from Resource.ApiLogin import ApiLogin

class RegisterView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.api = ApiLogin()
        self.username = ft.TextField(
            label="Usuario",
            helper_text="Ingrese su nombre de usuario",
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )
        self.name = ft.TextField(
            label="Nombre completo",
            helper_text="Ingrese su nombre completo",
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )
        self.password = ft.TextField(
            label="Contraseña",
            helper_text="Ingrese su contraseña",
            password=True,
            can_reveal_password=True,
            border_radius=ft.BorderRadius(5, 5, 5, 5),
        )

    def registrar_usuario(self, e):
        # Obtiene los valores de los campos de entrada
        nombre_completo = self.name.value
        usuario = self.username.value
        contrasena = self.password.value

        # Usa la API para guardar el usuario
        resultado = self.api.guardar_usuario(nombre_completo, usuario, contrasena)

        # Configura el SnackBar para mostrar el resultado
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                "Registro exitoso" if resultado["success"] else f"Error: {resultado['message']}"
            ),
            action="OK",
        )
        self.page.snack_bar.open = True  # Establece la propiedad `open` a True para mostrar el SnackBar
        self.page.update()

    def back(self, e):
        self.page.views.pop()
        self.page.update()

    def getRegisterView(self):
        title = ft.Text(
            value="Regístrate",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        register_button = ft.ElevatedButton(
            text="Registrar",
            on_click=self.registrar_usuario,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10,
            ),
        )

        backButton = ft.ElevatedButton(
            text="<--",
            on_click=self.back,
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
                title,
                ft.Container(padding=10),
                self.name,
                ft.Container(padding=10),
                self.username,
                ft.Container(padding=10),
                self.password,
                ft.Container(padding=5),
                ft.Row(
                    controls=[
                        register_button,
                        backButton,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            width=300,
        )

        login = ft.Row(
            controls=[
                ft.Container(
                    content=contente,
                    padding=20,
                    margin=ft.margin.only(top=30),
                )
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
            route="/Register",
            controls=[
                ft.Stack(
                    [
                        background,
                        contenido,
                    ],
                    width=self.page.width,
                )
            ],
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )
