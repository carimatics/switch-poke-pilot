import flet as ft

from switchpokepilot.app.ui.button import Button
from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.core.command.base import CommandInitParams
from switchpokepilot.core.command.implementations import command_classes
from switchpokepilot.core.state import AppState


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state

        # for command
        self._selected_command_index = 0
        self.stop_button: Button | None = None
        self.start_button: Button | None = None

    @property
    def is_running(self):
        return self.app_state.command_runner.is_running

    def did_mount(self):
        super().did_mount()
        self.app_state.controller.open("B001B8QO")

    def _update_button(self):
        self.stop_button.visible = self.is_running
        self.start_button.visible = not self.is_running
        self.update()

    def _start(self, button, e):
        params = CommandInitParams(controller=self.app_state.controller,
                                   logger=self.app_state.logger,
                                   camera=self.app_state.camera)
        self.app_state.command_runner.command = command_classes[self._selected_command_index](params=params)
        self.app_state.command_runner.start()
        self._update_button()

    def _stop(self, button, e):
        self.app_state.command_runner.stop()
        self.app_state.command_runner.command = None
        self._update_button()

    def _on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self._selected_command_index = index

    def build(self):
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
                             options=[command.NAME for command in command_classes],
                             value=command_classes[self._selected_command_index].NAME,
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
