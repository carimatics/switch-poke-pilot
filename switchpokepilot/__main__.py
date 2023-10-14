import flet as ft

from switchpokepilot.app.switchpokepilot import SwitchPokePilotApp
from switchpokepilot.utils.assets import get_assets_dir
from switchpokepilot.utils.env import is_packed

if __name__ == '__main__':
    packed = is_packed()
    app = SwitchPokePilotApp()
    ft.app(
        target=app.main,
        assets_dir=get_assets_dir(packed),
    )
