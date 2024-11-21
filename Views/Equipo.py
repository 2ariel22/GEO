import flet as ft
import asyncio
from Views.Reports import Reports
from Resource.ApiEquipo import ApiEquipo

class Equipo:
    def __init__(self, page: ft.Page):
        self.page = page
        self.navBar = self.getNavigation_bar()
        self.panel = None
        self.dateDevice = None  # Lista para almacenar la información del dispositivo
        self.deviceSelec={'0': 0}
        self.deviceToDelete = None
        self.reports = []
        self.api = ApiEquipo()
        self.defaulOptionsReports = [
                "caídas del equipo",
                "fallo al encender",
                "cortocircuito",
                "incapacidad de lectura \nde signos vitales",
                "mala calidad de imagen",
                "fallos en la impresión",
                "apagado sin razón aparente",
                "falta de imagen",
                "aparente fuga",
                "Otra..."
            ]

    def navigate(self, destination: ft.ControlEvent):
        if destination.data == "0":
            self.page.views.pop()
        elif destination.data == "1":
            self.page.views.pop()
            self.page.views.append(Reports(self.page, self.reports, self.navBar).getReports())
        elif destination.data == "2":
            self.page.views.pop()
           
        self.page.update()

    def getNavigation_bar(self):
        return ft.NavigationBar(
            selected_index=0, bgcolor='#efefef',
            destinations=[
                ft.NavigationDestination(icon=ft.icons.DEVICES, label="Equipos", data="0"),
                ft.NavigationDestination(icon=ft.icons.REPORT, label="Reportes", data="1"),
                ft.NavigationDestination(
                    icon=ft.icons.EXIT_TO_APP,
                    label="Salir",
                    data="2"
                ),
            ],
            on_change=self.navigate
        )

    def load_devices(self):
       # Utilizar el método obtener_equipos de ApiEquipo
       self.dateDevice = self.api.obtener_equipos()
       print(self.dateDevice)
       if self.dateDevice is not None:
            # Limpiar controles existentes, manteniendo el primer control (Add Device)
            aux = self.panel.controls[0]
            self.panel.controls.clear()
            self.panel.controls.append(aux)
            
            for device in self.dateDevice:
                self.panel.controls.append(self.generateEquipo(device['name'], device['location'], False))
                self.deviceSelec[str(len(self.panel.controls) -1)] = device['_id']
                self.page.update()
                
            print(self.deviceSelec)

    def back(self, e):
        self.page.views.pop()
        self.page.update()

    def generateEquipo(self, name, location, type):
        if type:
            exp = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_GREY_100,
                header=ft.ListTile(title=ft.Text(name)),
                expanded=True
            )

            exp.content = ft.ListTile(
                subtitle=ft.Text(f"Press the icon to {name}"),
                trailing=ft.IconButton(ft.icons.ADD, on_click=self.handleAdd, data=exp),
            )
            return exp
        else:
            exp = ft.ExpansionPanel(
                bgcolor=ft.colors.BLUE_GREY_100,
                header=ft.ListTile(title=ft.Text(f"Device: {name}\nLocation: {location}")),
            )

            exp.content = ft.Column(
                controls=[
                    ft.ListTile(
                        title=ft.Text(f"Press the icon to delete {name}"),
                        trailing=ft.IconButton(ft.icons.DELETE, on_click=self.handle_delete, data=exp),
                    ),
                    ft.ListTile(
                        title=ft.Text(f"Press this icon to see"),
                        trailing=ft.IconButton(ft.icons.FILE_OPEN_SHARP, on_click=self.handleSee, data=exp),
                    ),
                    ft.ListTile(
                        title=ft.Text(f"Press this icon to Create Report"),
                        trailing=ft.IconButton(ft.icons.CREATE, on_click=self.handle_Report, data=exp),
                    )
                ]
            )
            return exp

    def handle_Report(self, e:ft.ControlEvent):
        def button_clicked(e):
            if dd.value == "Otra...":
                otherOption.visible = True
            else:
                otherOption.visible = False
            self.page.update()

        otherOption = ft.TextField(
            visible=False,
            width=220,
            label="Other",
            autofill_hints=ft.AutofillHint.NAME,
        )
        
        listOption = [ft.dropdown.Option(option) for option in self.defaulOptionsReports]
        
        dd = ft.Dropdown(
            width=220,
            options=listOption,
            on_change=button_clicked
        )

        def handle_yes(e):
            for device in self.dateDevice:
                if self.deviceToDelete == device['_id']:
                    self.reports.append([device['name'],
                                    device['location'],
                                    True,
                                    dd.value])
                    self.reports.append([device['name'],
                                    device['location'],
                                    False,
                                    dd.value])
            self.page.close(dlg_modal)    
            self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Column(
                controls=[
                 ft.Row(
                     controls=[ft.Column(
                         controls=[ft.Text(value="Select your option"),
                                   dd,
                                   otherOption,
                                   ]
                     )],alignment=ft.MainAxisAlignment.CENTER
                 )
                ]
            ),
            actions=[
                ft.TextButton("Add", on_click=handle_yes),
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: self.page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )

        self.page.dialog = dlg_modal
        self.page.update()
        self.page.dialog.open = True
        self.page.update()
    
    def handle_change(self, e: ft.ControlEvent):
        print(f"change on panel with id {self.deviceSelec[e.data]}")
        self.deviceToDelete = self.deviceSelec[e.data]

    def handle_delete(self, e: ft.ControlEvent):
        # Eliminar dispositivo usando el método de ApiEquipo
        result = self.api.eliminar_equipo(self.deviceToDelete)
        if result:
            self.panel.controls.remove(e.control.data)
            self.page.update()
            # Recargar dispositivos después de eliminar
            self.load_devices()

    def handleAdd(self, e: ft.ControlEvent):
        name_field = ft.TextField(
            label="Name",
            autofill_hints=ft.AutofillHint.NAME,
        )
        
        location_field = ft.TextField(
            label="Location",
            autofill_hints=ft.AutofillHint.LOCATION,
        )
        serial_field = ft.TextField(
            label="Serial",
            autofill_hints=[ft.AutofillHint.CREDIT_CARD_NUMBER],
        )
        model_field = ft.TextField(
            label="Model",
            autofill_hints=[ft.AutofillHint.JOB_TITLE],
        )
        image_field = ft.TextField(
            label="Image",
            autofill_hints=ft.AutofillHint.URL,
        )
        
        def handle_yes(e):
            # Agregar dispositivo usando el método de ApiEquipo
            nuevo_id = self.api.agregar_equipo(
                name_field.value, 
                location_field.value, 
                serial_field.value, 
                model_field.value, 
                image_field.value
            )
            
            # Recargar dispositivos después de agregar
            self.page.close(dlg_modal)
            self.load_devices()
            self.page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            content=ft.Column(
                controls=[
                    name_field,
                    location_field,
                    serial_field,
                    model_field,
                    image_field,
                ]
            ),
            actions=[
                ft.TextButton("Add", on_click=handle_yes),
                ft.TextButton("Cancel", on_click=lambda e: self.page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: self.page.add(
                ft.Text("Modal dialog dismissed"),
            ),
        )

        self.page.dialog = dlg_modal
        self.page.update()
        self.page.dialog.open = True
        self.page.update()

    def handleSee(self, e: ft.ControlEvent):
        # Obtener dispositivo específico por ID usando ApiEquipo
        device = self.api.obtener_equipo_por_id(self.deviceToDelete)
        
        if device:
            name_field = ft.TextField(
                value= device['name'],
                label="Name",
                autofill_hints=ft.AutofillHint.NAME,
                read_only=True,
            )
            location_field = ft.TextField(
                value= device['location'],
                label="Location",
                autofill_hints=ft.AutofillHint.LOCATION,
                read_only=True,
            )
            serial_field = ft.TextField(
                value= device['serial'],
                label="Serial",
                autofill_hints=[ft.AutofillHint.CREDIT_CARD_NUMBER],
                read_only=True,
            )
            model_field = ft.TextField(
                value= device['model'],
                label="Model",
                autofill_hints=[ft.AutofillHint.JOB_TITLE],
                read_only=True,
            )
            image_field = ft.Image(
                src=device['img'],
                width=300,
                height=300,
                fit=ft.ImageFit.CONTAIN
            )
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Device"),
                content=ft.Column(
                    controls=[
                        name_field,
                        location_field,
                        serial_field,
                        model_field,
                        image_field,
                    ]
                ),
                actions=[
                    ft.TextButton("Close", on_click=lambda e: self.page.close(dlg_modal)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
                on_dismiss=lambda e: self.page.add(
                    ft.Text("Modal dialog dismissed"),
                ),
            )

            self.page.dialog = dlg_modal
            self.page.update()
            self.page.dialog.open = True
            self.page.update()

    def getEquipo(self):
        # El resto del método permanece igual
        title = ft.Text(
            value="Equipos",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=self.handle_change,
            controls=[
                self.generateEquipo("Add Device","lol", True),
            ]
        )

        self.page.add(ft.Text("Cargando dispositivos..."))
        
        self.page.add(self.panel)
        self.load_devices()
        self.page.update()

        backButton = ft.ElevatedButton(
            text="<--",
            on_click=self.back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10
            ),
        )

        contente = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                title,
                ft.Container(padding=10),
                ft.Container(padding=10),
                self.panel,
                ft.Container(padding=10),
                ft.Container(padding=5),
                ft.Row(controls=[
                    backButton
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER)
            ],
            width=300,
        )

        login = ft.Row(controls=[
            ft.Container(content=contente,
                         padding=20,
                         bgcolor='#ffffff',
                         border_radius=80,
                         width=300,
                         margin=ft.margin.only(top=30)
                         )
        ])

        background = ft.Container(
            width=self.page.width,
            height=(1 * self.page.height),
            bgcolor='#efefef',
            alignment=ft.alignment.center,
            padding=0,
            margin=0
        )

        contenido = ft.Row(controls=[login
                                     ],
                           alignment=ft.MainAxisAlignment.CENTER,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER,
                           )

        return ft.View(
            route="/Equipo",
            controls=[
                ft.Stack(
                    [
                        background,
                        contenido,
                    ], width=self.page.width,
                )
            ],
            navigation_bar=self.navBar,
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )