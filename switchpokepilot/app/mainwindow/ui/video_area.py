from typing import Optional

import flet as ft
from switch_pilot_core.camera import Camera

from switchpokepilot.app.mainwindow.state import MainWindowState
from switchpokepilot.app.ui.dropdown import Dropdown


class VideoArea(ft.UserControl):
    def __init__(self,
                 window_state: MainWindowState,
                 width: int,
                 height: int):
        super().__init__(width=width,
                         height=height,
                         animate_size=True)
        self._window_state = window_state

        self._active_camera: Optional[Camera] = window_state.camera
        self._devices = Camera.get_devices()

        self._dropdown: Optional[Dropdown] = None
        self._column: Optional[ft.Column] = None
        self._content: Optional[ft.Container] = None

    @property
    def _camera_options(self):
        return [device["name"] for device in self._devices]

    def resize(self, width: int, height: int):
        for control in [self._column, self._content, self]:
            control.width = width
            control.height = height
            control.update()

    def build(self):
        self._dropdown = Dropdown(label="Camera",
                                  value=self._active_camera.name,
                                  on_change=self._on_camera_change,
                                  options=self._camera_options,
                                  width=self.width)
        self._column = ft.Column(
            width=self.width,
            height=self.height,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[self._dropdown],
        )
        self._content = ft.Container(width=self.width,
                                     height=self.height,
                                     content=self._column,
                                     padding=ft.padding.all(2),
                                     alignment=ft.alignment.top_left)
        return self._content

    def _on_camera_change(self, _dropdown: Dropdown, _event: ft.ControlEvent, index: int):
        camera = Camera(capture_size=(1280, 720),
                        logger=self._window_state.logger)
        camera.name = self._devices[index]["name"]
        camera.id = self._devices[index]["id"]
        self._window_state.camera = camera
        self.update()
