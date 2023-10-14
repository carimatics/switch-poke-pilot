from typing import Callable, Self

import flet as ft

from switchpokepilot.ui.button import Button
from switchpokepilot.ui.dropdown import Dropdown


class CommandArea(ft.UserControl):
    def __init__(self, options: [str], on_command_changed: Callable[[Self, ft.ControlEvent, int], None]):
        super().__init__()
        self.contents: ft.Control | None = None

        self.options = options
        self.on_command_changed = on_command_changed

        self.is_stop = True
        self.stop_button: Button | None = None
        self.start_button: Button | None = None
        self.reload_button: Button | None = None

    def __update_button(self):
        self.stop_button.visible = not self.is_stop
        self.start_button.visible = self.is_stop
        self.reload_button.disabled = not self.is_stop
        self.update()

    def __start(self):
        self.is_stop = False
        self.__update_button()

    def __stop(self):
        self.is_stop = True
        self.__update_button()

    def build(self):
        def on_stop_clicked(button, e):
            self.__stop()

        def on_start_clicked(button, e):
            self.__start()

        self.stop_button = Button("Stop",
                                  on_click=on_stop_clicked,
                                  visible=not self.is_stop)
        self.start_button = Button("Start",
                                   on_click=on_start_clicked,
                                   visible=self.is_stop)
        self.reload_button = Button("Reload",
                                    disabled=not self.is_stop)

        self.contents = ft.Container(
            ft.Column(
                controls=[
                    Dropdown(label="Command",
                             options=self.options,
                             value=self.options[0],
                             on_change=lambda e: self.on_command_changed(self,
                                                                         e,
                                                                         self.options.index(e.data)),
                             width=200),
                    ft.Row(
                        controls=[
                            self.reload_button,
                            self.start_button,
                            self.stop_button,
                        ],
                    ),
                ]
            ),
            border=ft.border.all(width=2, color=ft.ColorScheme.surface_tint),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(8)
        )
        return self.contents
