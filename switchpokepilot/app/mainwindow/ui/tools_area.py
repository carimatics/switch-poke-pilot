from typing import Optional

import flet as ft

from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.app.mainwindow.ui.log_area import LogArea


class ToolsArea(ft.UserControl):
    def __init__(self,
                 window_state: MainWindowState,
                 width: int,
                 height: int):
        super().__init__(width=width, height=height)
        self._window_state = window_state

        self._indicators_height = 20

        self._container: Optional[ft.Container] = None
        self._area: Optional[ft.Tabs] = None
        self._tabs: list[ft.Tab] = []

    def build(self):
        self._tabs = [
            ft.Tab(icon=ft.icons.COMMENT,
                   content=LogArea(window_state=self._window_state,
                                   width=self.width,
                                   height=self.height - self._indicators_height)),
            ft.Tab(icon=ft.icons.VIDEOCAM),
            ft.Tab(icon=ft.icons.NAVIGATION),
            ft.Tab(icon=ft.icons.APP_REGISTRATION),
        ]
        self._area = ft.Tabs(selected_index=0,
                             width=self.width,
                             height=self.height,
                             indicator_padding=ft.padding.all(0),
                             animation_duration=300,
                             expand=True,
                             tabs=self._tabs)
        self._container = ft.Container(content=self._area,
                                       width=self.width,
                                       height=self.height,
                                       padding=ft.padding.all(0),
                                       margin=ft.margin.all(0),
                                       alignment=ft.alignment.top_left)
        return self._container

    def resize(self, width: int, height: int):
        self.width = width
        self.height = height

        for tab in self._tabs:
            if tab.content is not None:
                tab.content.resize(width, height - self._indicators_height)
                tab.content.update()

        for control in [self._area, self._container]:
            control.width = width
            control.height = height - self._indicators_height
            control.update()

        self.update()
