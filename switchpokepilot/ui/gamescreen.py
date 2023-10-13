import threading

import flet as ft

from switchpokepilot.camera import Camera

DISABLED_IMAGE = "/images/disabled.png"


class GameScreen(ft.UserControl):
    def __init__(self, camera: Camera, camera_id: int):
        super().__init__()

        # for loop
        self.th: threading.Thread | None = None

        # for camera
        self.camera: Camera = camera
        self.camera_id: int = camera_id

        self.screen: ft.Image | None = None

    def did_mount(self):
        self.camera.open(self.camera_id)
        self.th = threading.Thread(target=self.update_screen, args=(), daemon=True)
        self.th.start()

    def will_unmount(self):
        self.camera.destroy()

    def update_screen(self):
        while self.camera.is_opened():
            self.camera.read_frame()
            encoded = self.camera.encoded_current_frame_base64()
            if encoded == "":
                self.screen.src = DISABLED_IMAGE
                self.screen.src_base64 = None
            else:
                self.screen.src = None
                self.screen.src_base64 = encoded
            self.update()

    def build(self):
        self.screen = ft.Image(
            src=DISABLED_IMAGE,
            fit=ft.ImageFit.CONTAIN,
        )
        return self.screen
