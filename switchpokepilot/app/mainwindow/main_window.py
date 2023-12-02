import multiprocessing
from typing import Optional

import flet as ft

from switchpokepilot.app.info import get_app_info
from switchpokepilot.app.mainwindow.state import MainWindowState, MainWindowStateObserver
from switchpokepilot.app.mainwindow.ui.game_screen import GameScreen
from switchpokepilot.app.mainwindow.ui.tools_area import ToolsArea
from switchpokepilot.app.ui.theme import get_app_theme


class MainWindow(MainWindowStateObserver):
    def __init__(self, queue: multiprocessing.Queue):
        self._state = MainWindowState(queue=queue)

        self._page: Optional[ft.Page] = None
        self._app_info = get_app_info()

        self._expanded = True
        self._appbar_height = 35
        self._tools_area_width = 300
        self._tools_area: Optional[ToolsArea] = None
        self._game_screen: Optional[ft.Container] = None
        self._content: Optional[ft.Row] = None

    def main(self, page: ft.Page):
        self._page = page

        page.title = f"{self._app_info.name} {self._app_info.version}"
        page.on_resize = self._on_resize

        # page theme
        page.theme = get_app_theme()
        page.theme_mode = ft.ThemeMode.DARK

        page.padding = ft.padding.all(0)
        page.margin = ft.margin.all(0)
        page.expand = True

        # page layouts
        page.appbar = self._build_appbar()

        self._tools_area = ToolsArea(window_state=self._state,
                                     width=page.width,
                                     height=page.height - self._appbar_height)
        self._game_screen = ft.Container(content=GameScreen(window_state=self._state),
                                         width=page.width - self._tools_area_width,
                                         height=page.height,
                                         margin=ft.margin.all(0),
                                         padding=ft.padding.all(0),
                                         alignment=ft.alignment.top_left,
                                         border=ft.Border(),
                                         on_click=self._on_game_screen_click)
        self._content = ft.Row(controls=[self._game_screen, self._tools_area],
                               spacing=0,
                               alignment=ft.MainAxisAlignment.START,
                               vertical_alignment=ft.CrossAxisAlignment.START,
                               width=page.width,
                               height=page.height)
        page.add(self._content)

    def on_main_window_state_update(self, subject: MainWindowState):
        if self._state != subject:
            self._state = subject

    def _on_resize(self, _event: Optional[ft.ControlEvent] = None):
        height = self._page.height - self._appbar_height
        if self._expanded:
            self._game_screen.width = self._page.width - self._tools_area_width
            self._tools_area.resize(width=self._tools_area_width, height=height)
        else:
            self._game_screen.width = self._page.width
            self._tools_area.resize(width=0, height=height)
        self._game_screen.height = height

        # content
        self._content.width = self._page.width
        self._content.height = height

        self._page.update()

    def _build_appbar(self):
        appbar = ft.AppBar(toolbar_height=self._appbar_height,
                           actions=[
                               ft.IconButton(icon=ft.icons.CAMERA_ALT,
                                             tooltip="Take Screenshot",
                                             on_click=self._on_screenshot_click),
                               ft.IconButton(icon=ft.icons.SETTINGS,
                                             tooltip="Open Settings Modal",
                                             on_click=self._on_settings_click),
                           ])
        appbar.bgcolor = ft.colors.SURFACE_VARIANT
        return appbar

    def _on_game_screen_click(self, _event: ft.ControlEvent):
        self._state.logger.info("Game screen clicked")
        self._expanded = not self._expanded
        self._tools_area.visible = self._expanded
        self._tools_area.disabled = self._expanded
        self._on_resize()

    def _on_screenshot_click(self, _event: ft.ControlEvent):
        camera = self._state.camera
        if camera is not None and camera.is_opened():
            file_path = self._state.path.capture()
            camera.save_capture(file_path=file_path)
            self._state.logger.info(f"Capture saved: {file_path}")
        else:
            self._state.logger.debug("Camera not available")

    def _on_settings_click(self, _event: ft.ControlEvent):
        self._state.logger.debug(f"Settings clicked")
