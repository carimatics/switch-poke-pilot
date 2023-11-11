import threading

import flet as ft

from switchpokepilot.app.state import AppState, AppStateObserver
from switchpokepilot.core.camera import Camera

DISABLED_IMAGE = "/images/disabled.png"


class GameScreen(ft.UserControl, AppStateObserver):
    def __init__(self, app_state: AppState):
        super().__init__()
        self.screen: ft.Image | None = None
        self.app_state = app_state

        # for camera
        self.camera = self.app_state.camera

        # for loop
        self._thread: threading.Thread | None = None

    @property
    def camera(self) -> Camera | None:
        return self._get_attr("camera")

    @camera.setter
    def camera(self, new_value: Camera, dirty=True):
        self._set_attr("camera", new_value, dirty)

    def did_mount(self):
        self.app_state.add_observer(self)
        self._prepare_camera()

    def will_unmount(self):
        self.app_state.remove_observer(self)
        self._release_camera()

    def _prepare_camera(self):
        self.camera.open()
        self._thread = threading.Thread(target=self._loop_update_screen,
                                        name=f"{GameScreen.__name__}:{self._loop_update_screen.__name__}",
                                        daemon=True)
        self._thread.start()

    def _release_camera(self):
        self.camera.destroy()
        self._thread.join()
        self._thread = None

    def _loop_update_screen(self):
        while self.camera.is_opened():
            self.camera.update_frame()
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
            fit=ft.ImageFit.COVER,
            width=self.camera.capture_size[0],
            height=self.camera.capture_size[1],
        )
        return self.screen

    def on_app_state_update(self, subject: AppState) -> None:
        if self.camera != subject.camera:
            self.camera = subject.camera
            self._release_camera()
            self._prepare_camera()
        self.update()
