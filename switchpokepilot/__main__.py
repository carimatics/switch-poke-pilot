import flet as ft

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp
from switchpokepilot.core.utils.directories import get_assets_dir

if __name__ == '__main__':
    app = SwitchPokePilotApp()
    ft.app(
        target=app.main,
        assets_dir=get_assets_dir(),
    )
