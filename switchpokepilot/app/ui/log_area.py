import datetime

import flet as ft

from switchpokepilot.app.logger import AppLogger, LoggerObserver


class LogArea(ft.Container, LoggerObserver):
    def __init__(self, logger: AppLogger):
        self.text = ft.Text(f"Start: {datetime.datetime.now()}")
        super().__init__(
            width=600,
            height=910,
            content=ft.Column(
                width=600,
                height=910,
                scroll=ft.ScrollMode.ALWAYS,
                controls=[
                    self.text,
                ],
                auto_scroll=True,
            ),
            border=ft.border.all(2),
            alignment=ft.alignment.top_left,
        )
        self._logger = logger

    def did_mount(self):
        self._logger.add_observer(self)

    def will_unmount(self):
        self._logger.delete_observer(self)

    def add_log(self, message):
        if len(self.text.value) > 50000:
            self.text.value = f"{self.text.value[-10000:]}\n{message}"
        else:
            self.text.value = f"{self.text.value}\n{message}"
        self.update()

    def on_log(self, message):
        self.add_log(message)
