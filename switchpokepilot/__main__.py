import flet as ft

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp

if __name__ == '__main__':
    app = SwitchPokePilotApp()
    ft.app(
        target=app.main,
        assets_dir=app.path.user_directory(),
    )
