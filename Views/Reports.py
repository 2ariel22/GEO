import flet as ft

class Reports():

    def __init__(self, page: ft.Page,reports, navbar):
        self.page = page
        self.reports = reports
        self.navBar = navbar

    def back(self, e):
        self.page.views.pop()
        self.page.update()

    def generateEquipo(self, name,location,status, falla):
            color = None
            if(status):
                color = ft.colors.GREEN_400
            else:
                 color = ft.colors.RED_400
            exp = ft.ExpansionPanel(
                bgcolor=color,
                header=ft.ListTile(title=ft.Text(f"Device: {name}\nLocation: {location}")),
            )

            # Añadimos los botones en una columna
            exp.content = ft.Column(
                controls=[
                    ft.ListTile(
                        title=ft.Text(f"Falla {falla}"),
                        
                    ),
                   
                ]
            )
            return exp

   
    def getReports(self):
        title = ft.Text(
            value="Reports",
            style=ft.TextThemeStyle.HEADLINE_MEDIUM,
        )

        self.panel = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            #on_change=self.handle_change,
            
        )

        for x in self.reports:
             self.panel.controls.append(self.generateEquipo(x[0], x[1], x[2], x[3]))
             print(x)
             

        self.page.add(self.panel)
        
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
            route="/Reports",
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