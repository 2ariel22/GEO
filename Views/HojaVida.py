import flet as ft
import asyncio
import requests,json

from Views.Controls.OpcionesView import OpcionesView
from Resource.ApiEquipo import ApiEquipo
class HojaVida:
    def __init__(self, page: ft.Page):
        self.page = page
        self.opcionesView = None
        self.panel = None
        self.dateDevice = None  # Lista para almacenar la información del dispositivo
        self.deviceSelec={'0': 0}
        self.deviceToDelete = None
        self.api = ApiEquipo()


    def peticionDevice(self):
        data = self.api.obtener_equipos()
        print(data)
        return data
       
    def deleteDevice(self,id):
        self.api.eliminar_equipo(id)
       
           
        return True
       

    def addDeviceP(self,name_field,location_field, serial_field, model_field, image_field):
        data = self.api.agregar_equipo(name_field, location_field, serial_field, model_field, image_field)
       
        print(data)
        return data  # Retorna la respuesta si es exitosa
           

    def load_devices(self):
       self.dateDevice = self.peticionDevice()
       print(self.dateDevice)
       if(self.dateDevice != None):
            
            for device in self.dateDevice:
                
                self.panel.controls.append(self.generateEquipo(device['name'],device['location'], False))
                self.deviceSelec[str(len(self.panel.controls) -1)] = device['_id']
                self.page.update()
                
            print(self.deviceSelec)
    def back(self, e):
        self.page.views.pop()
        self.page.update()
    
    def handleCancel(self,e):
        self.page.close(e.control.parent)
    
    def handleMoreAbout(self,e):
        self.opcionesView = OpcionesView(self.page, self.handleSee, self.dateDevice, self.deviceToDelete)
        self.page.views.append(self.opcionesView.getOpcionesView())
        self.page.update()

    def generateEquipo(self, name,location, type):
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
            cupertino_actions = [
                ft.CupertinoDialogAction(
                    "Delete",
                    is_destructive_action=True,
                    on_click=self.handle_delete,
                    data=exp
                ),
                ft.CupertinoDialogAction(
                    text="Cancel",
                    is_default_action=False,
                    on_click=self.handleCancel,
                ),
            ]

            # Añadimos los botones en una columna
            exp.content = ft.Column(
                controls=[
                    ft.FilledTonalButton(
                        text="Delete",
                        on_click=lambda e: self.page.open(
                            ft.CupertinoAlertDialog(
                                title=ft.Text("Advertencia"),
                                content=ft.Text("Do you want to delete this file?"),
                                actions=cupertino_actions,
                                
                            ),
                        ),
                        icon=ft.icons.DELETE,
                        width=200,
                        
                    ),
                  
                   ft.FilledTonalButton(
                        text="More about",
                        icon=ft.icons.FILE_OPEN,
                        data=exp,
                        on_click=self.handleMoreAbout,
                        width=200
                    ),
                    ft.Container(padding=10)

                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                
            )
            return exp

   
    def handle_change(self, e: ft.ControlEvent):
        
        print(f"change on panel with index {self.deviceSelec[e.data]}")
        self.deviceToDelete = self.deviceSelec[e.data]

    def handle_delete(self, e: ft.ControlEvent):
        self.page.close(e.control.parent)
        self.panel.controls.remove(e.control.data)
        print(e.data)
        self.deleteDevice(self.deviceToDelete)
        self.page.update()

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
            self.dateDevice.append({
                "name": name_field.value,
                "location":location_field,
                "serial": serial_field.value,
                "model": model_field.value,
                "img": image_field.value,
            })
            self.addDeviceP(name_field.value,location_field.value,serial_field.value,model_field.value,image_field.value)
            print("Información del dispositivo guardada:", self.dateDevice)
            self.page.close(dlg_modal)
            self.panel.controls.clear()
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
        for device in self.dateDevice:
            if self.deviceToDelete == device['id']:
                print(device)

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
                testCg = ft.Text("Mantenimiento?:")
                cg = ft.RadioGroup(content=ft.Row([
                    ft.Radio(value="si", label="Si"),
                    ft.Radio(value="no", label="No")],
                    alignment=ft.MainAxisAlignment.CENTER))
                image_field = ft.Image(
                    src=device['img'],
                    width=300,            # Ancho fijo de 300 píxeles
                    height=300,           # Alto fijo de 300 píxeles
                    fit=ft.ImageFit.CONTAIN  # Ajusta la imagen dentro del contenedor sin distorsionarse
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
                            testCg,
                            cg,
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


    def getHojaVida(self):
        title = ft.Text(
            value="Equipos",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=self.handle_change,
           
        )
        
        
        self.page.add(self.panel)
        self.load_devices()
        self.page.update()

        backButton = ft.ElevatedButton( 
            text="back",
            icon=ft.icons.ARROW_BACK,  # Icono de flecha hacia atrás
            on_click=self.back,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=999),
                color="#292929",
                padding=10
            ),
        )

        addButton = ft.ElevatedButton(
            text="add",
            icon=ft.icons.ADD,  # Icono de más (+)
            on_click=self.handleAdd,
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
                ft.Row(controls=[
                    addButton,
                    backButton
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                
                ft.Container(padding=10),
                self.panel,
                ft.Container(padding=10),
                ft.Container(padding=5),
                
            ],
            width=300,
        )

        login = ft.Row(controls=[
            ft.Container(content=contente,
                         padding=20,
                         
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
            
            padding=0,
            scroll=ft.ScrollMode.AUTO,
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )