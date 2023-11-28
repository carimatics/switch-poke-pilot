import multiprocessing
from typing import Optional, Any

import flet as ft

from switchpokepilot.app.info import get_app_info
from switchpokepilot.app.main_window import MainWindow
from switchpokepilot.app.ui.theme import get_app_theme
from switchpokepilot.core.path.path import Path


def _open_main_window_app():
    window = MainWindow()
    path = Path()
    ft.app(
        port=0,
        target=window.main,
        assets_dir=path.user_directory(),
    )


class SwitchPokePilotApp:
    def __init__(self):
        self._info = get_app_info()
        self._page: Optional[ft.Page] = None
        self._content: Optional[ft.Control] = None
        self._buttons: list[ft.IconButton] = []
        self._settings_window: Optional[ft.FletApp] = None
        self._main_window_processes = []

    async def main(self, page: ft.Page):
        self._page = page

        page.title = f"{self._info.version}"
        page.theme = get_app_theme()
        page.theme_mode = ft.ThemeMode.DARK
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.window_width = 225
        page.window_height = 150
        page.window_resizable = False

        self._content = ft.Row(controls=self._buttons,
                               spacing=5,
                               width=page.window_width,
                               height=100,
                               alignment=ft.MainAxisAlignment.CENTER,
                               vertical_alignment=ft.CrossAxisAlignment.CENTER)
        self._buttons.append(self._create_settings_window_button())
        self._buttons.append(self._create_open_window_button())
        await page.add_async(self._content)

    async def _open_main_window(self, _event: ft.ControlEvent):
        process = multiprocessing.Process(target=_open_main_window_app, args=())
        self._main_window_processes.append(process)
        process.start()

    def _create_open_window_button(self):
        return self._create_button(icon=ft.icons.ADD_BOX,
                                   tooltip="Open new window",
                                   on_click=self._open_main_window)

    def _create_settings_window_button(self):
        return self._create_button(icon=ft.icons.SETTINGS,
                                   tooltip="Open settings window",
                                   on_click=self._open_main_window)

    @staticmethod
    def _create_button(icon: str, tooltip: str, on_click: Any):
        return ft.IconButton(icon=icon,
                             on_click=on_click,
                             tooltip=tooltip,
                             icon_color=ft.colors.ON_SURFACE,
                             icon_size=100,
                             width=100,
                             height=100,
                             style=ft.ButtonStyle(
                                 padding=0,
                             ))
