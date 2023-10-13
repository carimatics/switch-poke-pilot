import flet as ft

from switchpokepilot.app.switchpokepilot import SwitchPokePilotApp
from switchpokepilot.ui.gamescreen import GameScreen
from switchpokepilot.utils.assets import get_assets_dir
from switchpokepilot.utils.env import is_packed

NAME = "SwitchPokePilot"
VERSION = "v0.1.0"


def main(page: ft.Page):
    page.title = f"{NAME} {VERSION}"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    app = SwitchPokePilotApp()
    page.add(GameScreen(app.camera, camera_id=0))


if __name__ == '__main__':
    packed = is_packed()
    ft.app(
        target=main,
        assets_dir=get_assets_dir(packed)
    )
