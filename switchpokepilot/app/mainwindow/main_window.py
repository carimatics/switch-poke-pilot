import multiprocessing
from typing import Optional

import flet as ft

from switchpokepilot.app.info import get_app_info
from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.app.mainwindow.ui.game_screen import GameScreen
from switchpokepilot.app.mainwindow.ui.tools_area import ToolsArea
from switchpokepilot.app.ui.theme import get_app_theme


class MainWindow:
    def __init__(self, queue: multiprocessing.Queue):
        self._state = MainWindowState(queue=queue)

        self._page: Optional[ft.Page] = None
        self._app_info = get_app_info()

        self._expanded = True
        self._tools_area_width = 300
        self._tools_area: Optional[ToolsArea] = None
        self._game_screen: Optional[ft.Container] = None
        self._content: Optional[ft.Row] = None

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
        self._tools_area = ToolsArea(window_state=self._state,
                                     width=self._tools_area_width,
                                     height=page.height)
        self._game_screen = ft.Container(content=GameScreen(window_state=self._state),
                                         width=page.width - self._tools_area_width,
                                         height=page.height,
                                         margin=ft.margin.all(0),
                                         padding=ft.padding.all(0),
                                         alignment=ft.alignment.top_left,
                                         border=ft.Border(),
                                         on_click=self._on_game_screen_click)
        self._content = ft.Row(controls=[self._game_screen, self._tools_area],
                               spacing=0,
                               alignment=ft.MainAxisAlignment.START,
                               vertical_alignment=ft.CrossAxisAlignment.START,
                               width=page.width,
                               height=page.height)
        page.add(self._content)

    def _on_resize(self, _event: Optional[ft.ControlEvent] = None):
        if self._expanded:
            self._game_screen.width = self._page.width - self._tools_area_width
            self._tools_area.resize(width=self._tools_area_width,
                                    height=self._page.height)
        else:
            self._game_screen.width = self._page.width
            self._tools_area.resize(width=0, height=self._page.height)
        self._game_screen.height = self._page.height

        # content
        self._content.width = self._page.width
        self._content.height = self._page.height

        self._page.update()

    def _on_game_screen_click(self, _event: ft.ControlEvent):
        self._expanded = not self._expanded
        self._tools_area.visible = self._expanded
        self._tools_area.disabled = self._expanded
        self._on_resize()
