import flet as ft

from switchpokepilot.camera import Camera
from switchpokepilot.ui.capturearea import CaptureArea
from switchpokepilot.utils.assets import get_assets_dir
from switchpokepilot.utils.env import is_packed

NAME = "SwitchPokePilot"
VERSION = "v0.1.0"


def main(page: ft.Page):
    page.title = f"{NAME} {VERSION}"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def theme_clicked(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        page.update()

    # FIXME
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text(page.title),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=theme_clicked),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=lambda e: print("pushed")
                    ),
                ]
            ),
        ],
    )

    camera = Camera()
    page.add(
        CaptureArea(camera=camera, camera_id=0),
    )


if __name__ == '__main__':
    packed = is_packed()
    ft.app(
        target=main,
        assets_dir=get_assets_dir(packed)
    )
