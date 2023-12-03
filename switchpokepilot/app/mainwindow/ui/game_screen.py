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

        self._camera: Camera = self._window_state.camera
        self._screen: Optional[ft.Image] = None
        self._thread_update_loop: Optional[threading.Thread] = None

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
        if self._camera != subject.camera:
            self._release_camera()
            self._camera = subject.camera
            self._prepare_camera()
        self.update()

    def _prepare_camera(self):
        if self._camera is None:
            return

        if not self._camera.is_opened():
            self._camera.open()

        self._is_alive = True
        thread_name = f"{self.__class__.__name__}_{self._prepare_camera.__name__}_{id(self._camera)}"
        self._thread_update_loop = threading.Thread(target=self._loop_update_screen,
                                                    name=thread_name,
                                                    daemon=True)
        self._thread_update_loop.start()

    def _release_camera(self):
        self._is_alive = False
        if self._thread_update_loop is not None:
            self._thread_update_loop.join()
            self._thread_update_loop = None
            self._camera.release()

    def _loop_update_screen(self):
        camera = self._camera
        while self._is_alive and camera is not None and camera.is_opened():
            camera.update_frame()
            encoded = camera.encoded_current_frame_base64()
            if encoded == "":
                self._screen.src = DISABLED_IMAGE
                self._screen.src_base64 = None
            else:
                self._screen.src = None
                self._screen.src_base64 = encoded
            self.update()
