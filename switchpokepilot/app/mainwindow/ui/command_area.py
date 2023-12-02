from typing import Optional

import flet as ft

from switchpokepilot.api.command.command import CommandAPI
from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.core.command.loader import CommandLoader
from switchpokepilot.core.command.runner import CommandRunner
from switchpokepilot.core.libs.serial import SerialPort
from switchpokepilot.core.timer import Timer


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

        self._port_info = SerialPort.get_serial_ports()
        self._selected_port_index = 0
        self._port_dropdown: Optional[Dropdown] = None

        self._command_info = self._loader.get_info()
        self._selected_command_index = 0
        self._command_dropdown: Optional[Dropdown] = None

        self._reload_button: Optional[ft.ElevatedButton] = None
        self._start_button: Optional[ft.ElevatedButton] = None
        self._stop_button: Optional[ft.ElevatedButton] = None

    def resize(self, width: int, height: int):
        for control in [self._column, self._content, self]:
            control.width = width
            control.height = height
            control.update()

    def build(self):
        default_command_value = self._default_command_value()
        default_port_value = self._default_port_value()
        self._reload_button = ft.ElevatedButton(text="Reload",
                                                on_click=self._on_reload_click,
                                                icon=ft.icons.REFRESH_ROUNDED)
        self._start_button = ft.ElevatedButton(text="Start",
                                               icon=ft.icons.PLAY_ARROW_ROUNDED,
                                               on_click=self._on_start_click,
                                               visible=True)
        self._stop_button = ft.ElevatedButton(text="Stop",
                                              icon=ft.icons.STOP_ROUNDED,
                                              on_click=self._on_stop_click,
                                              visible=False)
        self._port_dropdown = Dropdown(label="Port",
                                       value=default_port_value,
                                       options=[port.name for port in self._port_info],
                                       width=self._dropdown_width,
                                       on_change=self._on_port_change)
        self._command_dropdown = Dropdown(label="Command",
                                          value=default_command_value,
                                          options=[info["config"]["name"] for info in self._command_info],
                                          width=self._dropdown_width,
                                          on_change=self._on_command_change)
        self._column = ft.Column(
            controls=[
                self._port_dropdown,
                self._command_dropdown,
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

    def _on_port_change(self, _dropdown: Dropdown, _event: ft.ControlEvent, index: int):
        self._selected_port_index = index

    def _on_command_change(self, _dropdown: Dropdown, _event: ft.ControlEvent, index: int):
        self._selected_command_index = index

    def _on_reload_click(self, _event: ft.ControlEvent):
        self._command_info = self._loader.get_info()
        self._command_dropdown.options = [info["config"]["name"] for info in self._command_info]
        self._command_dropdown.update()

    def _on_start_click(self, _event: ft.ControlEvent):
        self._runner.stop()
        port_info = self._port_info[self._selected_port_index]
        self._window_state.controller.open(port_info)
        self._runner.command = self._create_selected_command()
        self._runner.start(on_finish=self._on_command_finish)
        self._update_buttons()

    def _on_stop_click(self, _event: ft.ControlEvent):
        self._runner.stop()
        self._update_buttons()

    def _create_selected_command(self):
        info = self._command_info[self._selected_command_index]
        name = info["name"]
        api = CommandAPI(name=name,
                         logger=self._window_state.logger,
                         controller=self._window_state.controller,
                         config=self._window_state.config,
                         camera=self._window_state.camera,
                         path=self._window_state.path,
                         timer=Timer())
        command_class = self._loader.load(name)
        return command_class(api=api)

    def _on_command_finish(self):
        self._update_buttons()

    def _update_buttons(self):
        self._start_button.visible = not self._runner.is_running
        self._stop_button.visible = self._runner.is_running
        self.update()
