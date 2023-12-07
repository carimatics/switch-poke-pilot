from datetime import datetime
from typing import Optional

import flet as ft

from switchpokepilot.mainwindow.logger import MainWindowLoggerObserver
from switchpokepilot.mainwindow.state import MainWindowState


class LogArea(ft.UserControl, MainWindowLoggerObserver):
    def __init__(self,
                 window_state: MainWindowState,
                 width: int,
                 height: int):
        super().__init__(width=width,
                         height=height,
                         animate_size=True)
        self._window_state = window_state

        self._text: Optional[ft.Text] = None
        self._column: Optional[ft.Column] = None
        self._content: Optional[ft.Container] = None

    def resize(self, width: int, height: int):
        for control in [self._column, self._content, self]:
            control.width = width
            control.height = height
            control.update()

    def did_mount(self):
        self._window_state.logger.add_observer(self)

    def will_unmount(self):
        self._window_state.logger.remove_observer(self)

    def build(self):
        self._text = ft.Text(f"Start: {datetime.now()}",
                             selectable=True)
        self._column = ft.Column(
            width=self.width,
            height=self.height,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[self._text],
            auto_scroll=True,
        )
        self._content = ft.Container(width=self.width,
                                     height=self.height,
                                     content=self._column,
                                     padding=ft.padding.all(2),
                                     alignment=ft.alignment.top_left)
        return self._content

    def on_log(self, message: str):
        if len(self._text.value) > 50000:
            self._text.value = f"{self._text.value[-10000:]}\n{message}"
        else:
            self._text.value = f"{self._text.value}\n{message}"
        self._text.update()
