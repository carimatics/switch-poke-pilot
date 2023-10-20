import flet as ft

from switchpokepilot.app.ui.dropdown import Dropdown
from switchpokepilot.app.ui.game_screen import GameScreen
from switchpokepilot.core.camera import Camera
from switchpokepilot.core.state import AppState
from switchpokepilot.core.utils.device import get_devices


class CaptureArea(ft.UserControl):
    def __init__(self,
                 app_state: AppState):
        super().__init__()
        self.app_state = app_state

        self.contents: ft.Control | None = None

        self.active_camera: Camera | None = self.app_state.camera
        self.devices = get_devices()

    @property
    def _camera_options(self):
        return [device['name'] for device in self.devices]

    def _on_camera_change(self, dropdown: Dropdown, e: ft.ControlEvent, index: int):
        camera = Camera(capture_size=(1280, 720),
                        image_processor=self.app_state.image_processor,
                        logger=self.app_state.logger)
        camera.name = self.devices[index]['name']
        camera.id = self.devices[index]['id']
        self.app_state.camera = camera
        self.update()

    def build(self):
        self.contents = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            Dropdown(label="Camera",
                                     value=self.active_camera.name,
                                     on_change=self._on_camera_change,
                                     options=self._camera_options,
                                     width=800),
                        ],
                        width=1720,
                    ),
                    GameScreen(app_state=self.app_state),
                ],
                spacing=10,
                alignment=ft.alignment.top_left,
                horizontal_alignment=ft.alignment.top_left,
            ),
        )
        return self.contents
