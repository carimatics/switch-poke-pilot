import flet as ft

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp
from switchpokepilot.core.path.path import Path

if __name__ == '__main__':
    app = SwitchPokePilotApp()
    path = Path()
    ft.app(
        target=app.main,
        assets_dir=path.user_directory(),
    )
