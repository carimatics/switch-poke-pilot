import flet as ft

from switchpokepilot.commands.command import BaseCommand, CommandInitParams
from switchpokepilot.commands.loader import CommandLoader
from switchpokepilot.commands.runner import CommandRunner
from switchpokepilot.state import AppState
from switchpokepilot.ui.button import Button
from switchpokepilot.ui.dropdown import Dropdown


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state
        self.command_runner = CommandRunner()

        self.stop_button: Button | None = None
        self.start_button: Button | None = None
        self.reload_button: Button | None = None
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
        self.reload_button.disabled = self.is_running
        self.update()

    def _start(self, button, e):
        self.command_runner.command = self.app_state.command
        self.command_runner.start()
        self._update_button()

    def _stop(self, button, e):
        self.command_runner.stop()
        self.command_runner.command = None
        self._update_button()

    def _reload(self, button, e):
        self._reload_commands()
        self.update()

    def _reload_commands(self):
        command_dir = "./switchpokepilot/commands/implementations"
        params = CommandInitParams(controller=self.app_state.controller, logger=self.app_state.logger)
        self._commands = [Command(params=params) for Command in CommandLoader(command_dir).load()]

    def _on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self.app_state.command = self._commands[index]

    def _command(self, index: int):
        if index >= len(self._commands):
            return ""
        return self._commands[index]

    def build(self):
        self._reload_commands()
        self.stop_button = Button("Stop",
                                  on_click=self._stop,
                                  visible=self.is_running)
        self.start_button = Button("Start",
                                   on_click=self._start,
                                   visible=not self.is_running)
        self.reload_button = Button("Reload",
                                    on_click=self._reload,
                                    disabled=self.is_running)

        self.contents = ft.Container(
            ft.Column(
                controls=[
                    Dropdown(label="Command",
                             options=[command.name for command in self._commands],
                             value=self._command(0).name,
                             on_change=self._on_command_change,
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
