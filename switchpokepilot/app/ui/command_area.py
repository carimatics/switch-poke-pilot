import flet as ft

from switchpokepilot.app.ui.button import Button
from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.core.command.base import BaseCommand, CommandInitParams
from switchpokepilot.core.command.implementations import command_classes
from switchpokepilot.core.command.runner import CommandRunner
from switchpokepilot.core.state import AppState


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state
        self.command_runner = CommandRunner()

        self.stop_button: Button | None = None
        self.start_button: Button | None = None
        self._commands: list[BaseCommand] = []

    @property
    def is_running(self):
        return self.command_runner.is_running

    def did_mount(self):
        super().did_mount()
        self.app_state.controller.open("B001B8QO")

    def _update_button(self):
        self.stop_button.visible = self.is_running
        self.start_button.visible = not self.is_running
        self.update()

    def _start(self, button, e):
        self.command_runner.command = self.app_state.command
        self.command_runner.start()
        self._update_button()

    def _stop(self, button, e):
        self.command_runner.stop()
        self.command_runner.command = None
        self._update_button()

    def _initialize_commands(self):
        params = CommandInitParams(controller=self.app_state.controller,
                                   logger=self.app_state.logger,
                                   camera=self.app_state.camera)
        self._commands = [Command(params=params) for Command in command_classes]
        self.app_state.command = self._commands[0]

    def _on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self.app_state.command = self._commands[index]

    def build(self):
        self._initialize_commands()
        self.stop_button = Button("Stop",
                                  on_click=self._stop,
                                  visible=self.is_running)
        self.start_button = Button("Start",
                                   on_click=self._start,
                                   visible=not self.is_running)

        self.contents = ft.Container(
            ft.Column(
                controls=[
                    Dropdown(label="Command",
                             options=[command.name for command in self._commands],
                             value=self.app_state.command.name,
                             on_change=self._on_command_change,
                             width=200),
                    ft.Row(
                        controls=[
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
