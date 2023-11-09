from switchpokepilot.core.controller.state import ControllerState


class ControllerStateSerializer:
    @staticmethod
    def serialize(controller_state: ControllerState) -> str:
        str_l = ""
        str_r = ""

        flag_buttons = int(controller_state.buttons) << 2
        if controller_state.l_stick.changed:
            flag_buttons |= 0x2
            str_l = f"{format(controller_state.l_stick.x, "x")} {format(controller_state.l_stick.y, "x")}"
        if controller_state.r_stick.changed:
            flag_buttons |= 0x1
            str_r = f"{format(controller_state.r_stick.x, "x")} {format(controller_state.r_stick.y, "x")}"
        str_hat = str(int(controller_state.hat))

        return f"{format(flag_buttons, "#06x")} {str_hat} {str_l} {str_r}"
