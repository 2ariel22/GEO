import flet as ft
import requests
import json
from Resource.ApiEquipo import ApiEquipo

class OpcionesView():
    def __init__(self, page: ft.Page, handleSee, devices, deviceSelect):
        self.page = page
        self.handleSee = handleSee
        self.dateDevice = devices
        self.deviceToDelete = None
        self.api = ApiEquipo()
        
        # Buscar el dispositivo seleccionado en la lista de devices
        for device in devices:
            if device['_id'] == deviceSelect:
                self.deviceToDelete = device
                break

        # Inicializar los controles con los datos del dispositivo
        self.name_input = ft.TextField(
            label="Nombre",
            value=self.deviceToDelete.get('name', ''),
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        self.location_input = ft.TextField(
            label="Ubicación",
            value=self.deviceToDelete.get('location', ''),
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        self.serial_input = ft.TextField(
            label="Serial",
            value=self.deviceToDelete.get('serial', ''),
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        self.model_input = ft.TextField(
            label="Modelo",
            value=self.deviceToDelete.get('model', ''),
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        self.image_input = ft.TextField(
            label="URL de la imagen",
            value=self.deviceToDelete.get('img', ''),
            width=300,
            text_align=ft.TextAlign.CENTER
        )
        self.image_display = ft.Image(
            src=self.deviceToDelete.get('img', ''),
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )
        self.maintenance_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="true", label="En mantenimiento"),
                ft.Radio(value="false", label="Operativo")
            ], alignment=ft.MainAxisAlignment.CENTER),
            value=str(self.deviceToDelete.get('maintenance', False)).lower()
        )

    def back(self, e):
        self.page.views.pop()
        self.page.update()

    def hojaVida(self,e):
        self.page.update()

    def update_image_preview(self, e):
        self.image_display.src = self.image_input.value
        self.page.update()

    def update_device(self, updated_data):
        data = self.api.actualizar_equipo(self.deviceToDelete['_id'], updated_data)
 
        print(data)
        return True
    

    def save_changes(self, e):
        updated_data = {
            'name': self.name_input.value,
            'location': self.location_input.value,
            'serial': self.serial_input.value,
            'model': self.model_input.value,
            'maintenance': self.maintenance_radio.value == "true",
            'img': self.image_input.value
        }

        if self.update_device(updated_data):
            self.deviceToDelete.update(updated_data)
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Cambios guardados correctamente"))
            )
        else:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Error al guardar los cambios"))
            )
        self.page.update()

    def getOpcionesView(self):
        title = ft.Text(
            value="Editar Dispositivo",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
            text_align=ft.TextAlign.CENTER,
            width=400
        )
        
        # Formulario de edición
        edit_form = ft.Column(
            controls=[
                self.name_input,
                ft.Container(padding=5),
                self.location_input,
                ft.Container(padding=5),
                self.serial_input,
                ft.Container(padding=5),
                self.model_input,
                ft.Container(padding=5),
                self.image_input,
                ft.ElevatedButton(
                    text="Actualizar vista previa",
                    on_click=self.update_image_preview,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=999),
                        color="#292929",
                        padding=10
                    ),
                ),
                ft.Container(padding=5),
                self.image_display,
                ft.Container(padding=10),
                ft.Text(
                    "Estado de mantenimiento:", 
                    size=16, 
                    text_align=ft.TextAlign.CENTER,
                    width=400
                ),
                self.maintenance_radio,
                ft.Container(padding=10),
                ft.ElevatedButton(
                    text="Guardar cambios",
                    on_click=self.save_changes,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=999),
                        color="#292929",
                        padding=10
                    ),
                )
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
                ft.Container(padding=20),
                edit_form,
                ft.Container(padding=20),
                backButton,
            ],
            width=400,
        )
        
        login = ft.Row(
            controls=[ft.Container(content=contente, padding=20)],
            alignment=ft.MainAxisAlignment.CENTER
        )

        background = ft.Container(
            width=self.page.width,
            height=(1*self.page.height),
            #bgcolor='#efefef',
            alignment=ft.alignment.center,
            padding=0,
            margin=0
        )

        contenido = ft.Row(
            controls=[login], 
            alignment=ft.MainAxisAlignment.CENTER, 
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

        return ft.View(
            route="/Opciones",
            controls=[
                ft.Stack(
                    [background, contenido],
                    width=self.page.width,
                    alignment=ft.alignment.center
                )
            ],
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )