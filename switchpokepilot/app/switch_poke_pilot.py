from dataclasses import dataclass

import flet as ft

from switchpokepilot.app.state import AppState, AppStateObserver
from switchpokepilot.app.ui.appbar import AppBar
from switchpokepilot.app.ui.capture_area import CaptureArea
from switchpokepilot.app.ui.command_area import CommandArea
from switchpokepilot.app.ui.log_area import LogArea
from switchpokepilot.core.camera import Camera
from switchpokepilot.core.utils.device import get_devices

NAME = "SwitchPokePilot"
VERSION = {
    "major": 0,
    "minor": 1,
    "patch": 0,
}


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"


class SwitchPokePilotApp(AppStateObserver):
    def __init__(self):
        self.version = Version(major=VERSION["major"],
                               minor=VERSION["minor"],
                               patch=VERSION["patch"])
        self.state = AppState()
        self.page: ft.Page | None = None
        self.content: ft.Control | None = None

    def create_default_camera(self):
        camera = Camera(capture_size=self.state.capture_size,
                        logger=self.state.logger)
        camera_info = get_devices()[0]
        camera.id = camera_info['id']
        camera.name = camera_info['name']
        return camera

    def main(self, page: ft.Page):
        self.state.camera = self.create_default_camera()
        self.state.add_observer(self)

        self.page = page

        self.page.title = f"{NAME} {self.version}"
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START

        self.page.appbar = AppBar(page=page)

        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            CaptureArea(app_state=self.state),
                            CommandArea(app_state=self.state),
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
