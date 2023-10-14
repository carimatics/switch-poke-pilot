import flet as ft


class AppBar(ft.AppBar):
    def __init__(self, page):
        # FIXME
        super().__init__(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text(page.title),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=self.theme_click),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False, on_click=lambda e: print("pushed")
                        ),
                    ]
                ),
            ],
        )
        self.page = page

    def theme_click(self, e):
        if self.page.theme_mode == ft.ThemeMode.DARK:
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.DARK
        self.page.update()
