import flet as ft

from switchpokepilot.app.state import AppState
from switchpokepilot.app.ui.button import Button
from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.core.command.base import CommandInitParams, Command
from switchpokepilot.core.command.implementations import command_classes


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state

        # for command
        self._selected_command_index = 0
        self._start_button: Button | None = None
        self._stop_button: Button | None = None

    @property
    def runner(self):
        return self.app_state.command_runner

    @property
    def command(self):
        return self.runner.command

    @command.setter
    def command(self, new_value: Command):
        self.runner.command = new_value

    def did_mount(self):
        super().did_mount()
        self.app_state.controller.open("B001B8QO")

    def _update_buttons(self):
        self._start_button.visible = not self.runner.is_running
        self._stop_button.visible = self.runner.is_running
        self.update()

    def _on_command_finish(self):
        self._update_buttons()

    def _on_start_click(self, button, e):
        self.runner.stop()
        self.command = self._create_selected_command()
        self.runner.start(on_finish=self._on_command_finish)
        self._update_buttons()

    def _on_stop_click(self, button, e):
        self.runner.stop()
        self._update_buttons()

    def _on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self._selected_command_index = index

    def _create_selected_command(self):
        params = CommandInitParams(controller=self.app_state.controller,
                                   logger=self.app_state.logger,
                                   camera=self.app_state.camera)
        return command_classes[self._selected_command_index](params=params)

    def build(self):
        self._start_button = Button("Start",
                                    on_click=self._on_start_click,
                                    visible=True)
        self._stop_button = Button("Stop",
                                   on_click=self._on_stop_click,
                                   visible=False)

        self.contents = ft.Container(
            ft.Column(
                controls=[
                    Dropdown(label="Command",
                             options=[command.NAME for command in command_classes],
                             value=command_classes[self._selected_command_index].NAME,
                             on_change=self._on_command_change,
                             width=200),
                    ft.Row(
                        controls=[
                            self._start_button,
                            self._stop_button,
                        ],
                    ),
                ]
            ),
            border=ft.border.all(width=2, color=ft.ColorScheme.surface_tint),
            border_radius=ft.border_radius.all(10),
            padding=ft.padding.all(8)
        )
        return self.contents
