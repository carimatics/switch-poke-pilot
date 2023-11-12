import flet as ft

from switchpokepilot.app.switch_poke_pilot import SwitchPokePilotApp

if __name__ == '__main__':
    app = SwitchPokePilotApp()
    ft.app(
        target=app.main,
        assets_dir=app.state.path.user_directory(),
    )
