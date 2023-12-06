from multiprocessing import freeze_support

import flet as ft
from switch_pilot_core.path import Path

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp

if __name__ == '__main__':
    freeze_support()

    app = SwitchPokePilotApp()
    path = Path()
    ft.app(
        target=app.main,
        assets_dir=path.user_directory(),
    )
