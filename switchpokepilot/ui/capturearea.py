import flet as ft

from switchpokepilot.camera import Camera
from switchpokepilot.ui.dropdown import Dropdown
from switchpokepilot.ui.gamescreen import GameScreen


class CaptureArea(ft.UserControl):
    def __init__(self,
                 camera: Camera,
                 camera_id: int):
        super().__init__()
        self.camera = camera
        self.camera_id = camera_id

    def build(self):
        # FIXME
        cameras = ["A", "B", "C"]
        camera_name = cameras[0]

        def on_camera_changed(dropdown: Dropdown, e: ft.ControlEvent, index: int):
            print(e.data)
            print(index)
            dropdown.update()

        return ft.Column(
            controls=[
                Dropdown(label="Camera",
                         value=camera_name,
                         on_change=on_camera_changed,
                         options=cameras),
                GameScreen(self.camera, camera_id=self.camera_id),
            ],
            spacing=10,
            alignment=ft.alignment.top_left,
            horizontal_alignment=ft.alignment.top_left,
        )
