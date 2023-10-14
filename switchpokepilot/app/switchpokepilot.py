import flet as ft

from switchpokepilot.camera import Camera
from switchpokepilot.state import AppState, AppStateObserver
from switchpokepilot.ui.appbar import AppBar
from switchpokepilot.ui.capturearea import CaptureArea
from switchpokepilot.ui.commandarea import CommandArea
from switchpokepilot.ui.dropdown import Dropdown
from switchpokepilot.ui.logarea import LogArea
from switchpokepilot.utils.device import get_devices

NAME = "SwitchPokePilot"
VERSION = "v0.1.0"


class SwitchPokePilotApp(AppStateObserver):
    def __init__(self):
        self.state = AppState()
        self.page: ft.Page | None = None
        self.content: ft.Control | None = None

    def on_command_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        pass

    def create_default_camera(self):
        camera = Camera(capture_size=self.state.capture_size)
        camera_info = get_devices()[0]
        camera.id = camera_info['id']
        camera.name = camera_info['name']
        return camera

    def main(self, page: ft.Page):
        self.state.camera = self.create_default_camera()
        self.state.add_observer(self)

        self.page = page

        self.page.title = f"{NAME} {VERSION}"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START

        self.page.appbar = AppBar(page=page)

        command_options = ["自動リーグ周回", "無限きのみ"]

        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            CaptureArea(app_state=self.state),
                            CommandArea(app_state=self.state,
                                        options=command_options,
                                        on_command_changed=self.on_command_change),
                        ],
                        width=1280,
                    ),
                    LogArea(self.state.logger),
                ],
            ),
            alignment=ft.alignment.top_left,
        )
        page.add(self.content)

    def on_app_state_update(self, subject: AppState) -> None:
        self.state.logger.debug("SwitchPokePilotApp: on_app_state_update")
