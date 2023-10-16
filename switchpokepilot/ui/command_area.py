from typing import Callable

import flet as ft

from switchpokepilot.commands.implementations.mash_a import MashA
from switchpokepilot.commands.runner import CommandRunner
from switchpokepilot.state import AppState
from switchpokepilot.ui.button import Button
from switchpokepilot.ui.dropdown import Dropdown


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState,
                 options: [str],
                 on_command_changed: Callable[[Dropdown, ft.ControlEvent, int], None]):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state
        self.command_runner = CommandRunner()

        self.options = options
        self.on_command_changed = on_command_changed

        self.stop_button: Button | None = None
        self.start_button: Button | None = None
        self.reload_button: Button | None = None

    @property
    def is_running(self):
        if self.command_runner.command is None:
            return False
        return self.command_runner.command.is_running

    def did_mount(self):
        super().did_mount()
        self.app_state.controller.open("B001B8QO")
        self.app_state.command = MashA(controller=self.app_state.controller)

    def __update_button(self):
        self.stop_button.visible = self.is_running
        self.start_button.visible = not self.is_running
        self.reload_button.disabled = self.is_running
        self.stop_button.update()
        self.start_button.update()
        self.reload_button.update()

    def __start(self, button, e):
        self.command_runner.command = self.app_state.command
        self.command_runner.start()
        self.__update_button()

    def __stop(self, button, e):
        self.command_runner.stop()
        self.command_runner.command = None
        self.__update_button()

    def build(self):
        self.stop_button = Button("Stop",
                                  on_click=self.__stop,
                                  visible=self.is_running)
        self.start_button = Button("Start",
                                   on_click=self.__start,
                                   visible=not self.is_running)
        self.reload_button = Button("Reload",
                                    disabled=self.is_running)

        self.contents = ft.Container(
            ft.Column(
                controls=[
                    Dropdown(label="Command",
                             options=self.options,
                             value=self.options[0],
                             on_change=self.on_command_changed,
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
