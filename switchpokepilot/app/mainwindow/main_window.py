import multiprocessing
from typing import Optional

import flet as ft

from switchpokepilot.app.info import get_app_info
from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.app.mainwindow.ui.game_screen import GameScreen
from switchpokepilot.app.ui.theme import get_app_theme

DISABLED_IMAGE = "/images/no_image_available.png"


class MainWindow:
    def __init__(self, queue: multiprocessing.Queue):
        self._state = MainWindowState(queue=queue)

        self._page: Optional[ft.Page] = None
        self._app_info = get_app_info()

        self._game_screen: Optional[ft.Container] = None

    def main(self, page: ft.Page):
        self._page = page

        page.title = f"{self._app_info.name} {self._app_info.version}"
        page.on_resize = self._on_resize

        # page theme
        page.theme = get_app_theme()
        page.theme_mode = ft.ThemeMode.DARK

        page.padding = ft.padding.all(0)
        page.margin = ft.margin.all(0)
        page.expand = True

        # page layouts
        page.appbar = ft.AppBar(title=ft.Text(value=page.title,
                                              size=18),
                                toolbar_height=35,
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                actions=[
                                    ft.IconButton(icon=ft.icons.CAMERA_ALT),
                                ])

        self._game_screen = ft.Container(content=GameScreen(window_state=self._state),
                                         width=page.width,
                                         height=page.height - page.appbar.toolbar_height,
                                         margin=ft.margin.all(0),
                                         padding=ft.padding.all(0),
                                         alignment=ft.alignment.top_left)
        tool_area = ft.Column(controls=[],
                              width=250,
                              height=page.height)
        content = ft.Row(controls=[self._game_screen, tool_area],
                         spacing=0,
                         alignment=ft.MainAxisAlignment.START,
                         vertical_alignment=ft.CrossAxisAlignment.START,
                         width=page.width,
                         height=page.height)
        page.add(content)

    def _on_resize(self, e: ft.ControlEvent):
        self._game_screen.height = self._page.height - self._page.appbar.toolbar_height
        self._game_screen.width = self._page.width
        self._game_screen.update()
