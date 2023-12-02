import threading
from typing import Optional

import flet as ft

from switchpokepilot.app.mainwindow.state import MainWindowStateObserver, MainWindowState
from switchpokepilot.core.camera import Camera

DISABLED_IMAGE = "/images/no_image_available.png"


class GameScreen(ft.UserControl, MainWindowStateObserver):
    def __init__(self, window_state: MainWindowState):
        super().__init__()
        self._is_alive: bool = True
        self._window_state = window_state

        self.camera = self._window_state.camera
        self._screen: Optional[ft.Image] = None
        self._thread_update_loop: Optional[threading.Thread] = None

    @property
    def camera(self) -> Optional[Camera]:
        return self._get_attr("camera")

    @camera.setter
    def camera(self, new_value: Camera, dirty=True):
        self._set_attr("camera", new_value, dirty)

    def did_mount(self):
        self._window_state.add_observer(self)
        self._prepare_camera()

    def will_unmount(self):
        self._window_state.remove_observer(self)
        self._release_camera()

    def build(self):
        self._screen = ft.Image(src=DISABLED_IMAGE,
                                fit=ft.ImageFit.FILL)
        return self._screen

    def on_main_window_state_update(self, subject: MainWindowState) -> None:
        if self.camera != subject.camera:
            self.camera = subject.camera
            self._release_camera()
            self._prepare_camera()
        self.update()

    def _loop_update_screen(self):
        while self._is_alive and self.camera is not None and self.camera.is_opened():
            self.camera.update_frame()
            encoded = self.camera.encoded_current_frame_base64()
            if encoded == "":
                self._screen.src = DISABLED_IMAGE
                self._screen.src_base64 = None
            else:
                self._screen.src = None
                self._screen.src_base64 = encoded
            self.update()

    def _prepare_camera(self):
        if self.camera is None:
            # FIXME
            self.camera = Camera(capture_size=(1280, 720),
                                 logger=self._window_state.logger)
            self._window_state.camera = self.camera
        self.camera.open()
        self._thread_update_loop = threading.Thread(target=self._loop_update_screen,
                                                    daemon=True)
        self._thread_update_loop.start()

    def _release_camera(self):
        self._is_alive = False
        self._thread_update_loop.join()
        self._thread_update_loop = None
