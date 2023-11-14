import flet as ft

from switchpokepilot.api.command.command import CommandAPI
from switchpokepilot.app.state import AppState
from switchpokepilot.app.ui.button import Button
from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.core.command.loader import CommandLoader
from switchpokepilot.core.libs.serial import SerialPort
from switchpokepilot.core.timer import Timer


class CommandArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.contents: ft.Control | None = None
        self.app_state = app_state

        # for command
        self._command_loader = CommandLoader(config=self.app_state.config)
        self._command_info = self._command_loader.get_info()
        self._selected_command_index = 0
        self._start_button: Button | None = None
        self._stop_button: Button | None = None
        self._port_info = SerialPort.get_serial_ports()
        self._selected_port_index = 0

    @property
    def runner(self):
        return self.app_state.command_runner

    def _update_buttons(self):
        self._start_button.visible = not self.runner.is_running
        self._stop_button.visible = self.runner.is_running
        self.update()

    def _on_command_finish(self):
        self._update_buttons()

    def _on_start_click(self, button, e):
        self.runner.stop()
        port_info = self._port_info[self._selected_port_index]
        self.app_state.controller.open(port_info)
        self.runner.command = self._create_selected_command()
        self.runner.start(on_finish=self._on_command_finish)
        self._update_buttons()

    def _on_stop_click(self, button, e):
        self.runner.stop()
        self._update_buttons()

    def _on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self._selected_command_index = index

    def _on_port_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        self._selected_port_index = index

    def _create_selected_command(self):
        info = self._command_info[self._selected_command_index]
        name = info["name"]
        api = CommandAPI(name=name,
                         logger=self.app_state.logger,
                         controller=self.app_state.controller,
                         config=self.app_state.config,
                         camera=self.app_state.camera,
                         path=self.app_state.path,
                         timer=Timer())
        command_class = self._command_loader.load(name)
        return command_class(api=api)

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
                    ft.Row(
                        controls=[
                            Dropdown(label="Command",
                                     options=[info["config"]["name"] for info in self._command_info],
                                     value=self._command_info[self._selected_command_index]["name"],
                                     on_change=self._on_command_change,
                                     width=200),
                            Dropdown(label="PortInfo",
                                     options=[info.name for info in self._port_info],
                                     value=self._port_info[self._selected_port_index].name,
                                     on_change=self._on_port_change,
                                     width=100),
                        ],
                        width=1720,
                    ),
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
