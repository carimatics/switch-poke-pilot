from switchpokepilot.core.controller.button import Button
from switchpokepilot.core.controller.hat import Hat
from switchpokepilot.core.controller.stick import STICK_DISPLACEMENT_RANGE, Stick, StickDisplacement


class ControllerState:
    def __init__(self,
                 buttons=0,
                 hat=Hat.CENTER,
                 lx=STICK_DISPLACEMENT_RANGE["center"],
                 ly=STICK_DISPLACEMENT_RANGE["center"],
                 l_stick_changed=False,
                 rx=STICK_DISPLACEMENT_RANGE["center"],
                 ry=STICK_DISPLACEMENT_RANGE["center"],
                 r_stick_changed=False):
        self.buttons = buttons
        self.hat = hat

        # L stick
        self.l_stick = Stick()
        self.l_stick.x = lx
        self.l_stick.y = ly
        self.l_stick.changed = l_stick_changed

        # R stick
        self.r_stick = Stick()
        self.r_stick.x = rx
        self.r_stick.y = ry
        self.r_stick.changed = r_stick_changed

    def set(self,
            buttons: list[Button] | None = None,
            l_displacement: StickDisplacement | None = None,
            r_displacement: StickDisplacement | None = None,
            hat: Hat | None = None):
        if buttons is not None:
            for button in buttons:
                self.buttons |= button

        if l_displacement is not None:
            self.l_stick.set_displacement(l_displacement)
        if r_displacement is not None:
            self.r_stick.set_displacement(r_displacement)

        if hat is not None:
            self.hat = hat

    def unset(self,
              buttons: list[Button] | None = None):
        if buttons is not None:
            for button in buttons:
                self.buttons &= ~button

    def reset_buttons(self):
        self.buttons = 0

    def reset_stick_displacement(self):
        self.l_stick.reset()
        self.r_stick.reset()

    def consume_stick_displacement(self):
        self.l_stick.consume()
        self.r_stick.consume()

    def reset_hat(self):
        self.hat = Hat.CENTER

    def reset(self):
        self.reset_buttons()
        self.reset_stick_displacement()
        self.reset_hat()

    def copy(self):
        return ControllerState(
            buttons=self.buttons,
            hat=self.hat,
            lx=self.l_stick.x,
            ly=self.l_stick.y,
            l_stick_changed=self.l_stick.changed,
            rx=self.r_stick.x,
            ry=self.r_stick.y,
            r_stick_changed=self.r_stick.changed)
