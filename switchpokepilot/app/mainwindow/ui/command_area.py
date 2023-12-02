from typing import Optional

import flet as ft

from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.core.command.loader import CommandLoader
from switchpokepilot.core.command.runner import CommandRunner
from switchpokepilot.core.libs.serial import SerialPort


class CommandArea(ft.UserControl):
    def __init__(self,
                 window_state: MainWindowState,
                 width: int,
                 height: int):
        super().__init__(width=width,
                         height=height,
                         animate_size=True)
        self._window_state = window_state

        self._loader = CommandLoader(config=self._window_state.config,
                                     path=self._window_state.path)
        self._runner = CommandRunner()

        self._dropdown_width = self.width

        self._content: Optional[ft.Container] = None
        self._column: Optional[ft.Column] = None

        self._command_info = self._loader.get_info()
        self._selected_command_index = 0
        self._reload_button: Optional[ft.ElevatedButton] = None
        self._start_button: Optional[ft.ElevatedButton] = None
        self._stop_button: Optional[ft.ElevatedButton] = None
        self._port_info = SerialPort.get_serial_ports()
        self._selected_port_index = 0

    def resize(self, width: int, height: int):
        for control in [self._column, self._content, self]:
            control.width = width
            control.height = height
            control.update()

    def build(self):
        default_command_value = self._default_command_value()
        default_port_value = self._default_port_value()
        self._reload_button = ft.ElevatedButton(text="Reload",
                                                icon=ft.icons.REFRESH_ROUNDED)
        self._start_button = ft.ElevatedButton(text="Start",
                                               icon=ft.icons.PLAY_ARROW_ROUNDED,
                                               visible=True)
        self._stop_button = ft.ElevatedButton(text="Stop",
                                              icon=ft.icons.STOP_ROUNDED,
                                              visible=False)
        self._column = ft.Column(
            controls=[
                ft.Dropdown(
                    label="Port",
                    value=default_port_value,
                    options=[ft.dropdown.Option(port.name) for port in self._port_info],
                    width=self._dropdown_width,
                ),
                ft.Dropdown(
                    label="Command",
                    value=default_command_value,
                    options=[ft.dropdown.Option(info["config"]["name"]) for info in self._command_info],
                    width=self._dropdown_width,
                ),
                ft.Row(
                    controls=[self._reload_button, self._start_button, self._stop_button],
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self._content = ft.Container(content=self._column,
                                     padding=ft.padding.all(4))
        return self._content

    def _default_command_value(self):
        if len(self._command_info) <= self._selected_command_index:
            return "Command not found"
        return self._command_info[self._selected_command_index]["config"]["name"]

    def _default_port_value(self):
        if len(self._port_info) <= self._selected_port_index:
            return "Port not found"
        return self._port_info[self._selected_port_index].name
