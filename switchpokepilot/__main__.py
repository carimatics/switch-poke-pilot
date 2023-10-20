import flet as ft

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp
from switchpokepilot.core.utils.assets import get_assets_dir
from switchpokepilot.core.utils.env import is_packed

if __name__ == '__main__':
    packed = is_packed()
    app = SwitchPokePilotApp()
    ft.app(
        target=app.main,
        assets_dir=get_assets_dir(packed),
    )
