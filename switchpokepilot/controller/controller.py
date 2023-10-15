import time
from enum import Enum, IntEnum, IntFlag, auto
from time import sleep

from switchpokepilot.controller.serial import Serial
from switchpokepilot.logger import Logger


class Button(IntFlag):
    Y = auto()
    B = auto()
    A = auto()
    X = auto()
    L = auto()
    R = auto()
    ZL = auto()
    ZR = auto()
    MINUS = auto()
    PLUS = auto()
    L_CLICK = auto()
    R_CLICK = auto()
    HOME = auto()
    CAPTURE = auto()


class Hat(IntEnum):
    TOP = 0
    TOP_RIGHT = auto()
    RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM = auto()
    BOTTOM_LEFT = auto()
    LEFT = auto()
    TOP_LEFT = auto()
    CENTER = auto()


class Stick(Enum):
    LEFT = auto()
    RIGHT = auto()


class Tilt(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    R_UP = auto()
    R_RIGHT = auto()
    R_DOWN = auto()
    R_LEFT = auto()


STICK_RANGE = {
    "min": 0,
    "center": 128,
    "max": 255,
}


class ControllerState:
    def __init__(self,
                 buttons=0,
                 hat=Hat.CENTER,
                 lx=STICK_RANGE["center"],
                 ly=STICK_RANGE["center"],
                 rx=STICK_RANGE["center"],
                 ry=STICK_RANGE["center"],
                 l_stick_changed=False,
                 r_stick_changed=False):
        self.buttons = buttons
        self.hat = hat
        self.lx = lx
        self.ly = ly
        self.rx = rx
        self.ry = ry
        self.l_stick_changed = l_stick_changed
        self.r_stick_changed = r_stick_changed

    def set(self,
            buttons: list[Button] | None = None,
            hat: Hat | None = None):
        if buttons is not None:
            for button in buttons:
                self.buttons |= button
        if hat is not None:
            self.hat = hat

    def unset(self,
              buttons: list[Button] | None = None):
        if buttons is not None:
            for button in buttons:
                self.buttons &= ~button

    def reset_buttons(self):
        self.buttons = 0

    def reset_directions(self):
        self.reset_hat()
        self.lx = STICK_RANGE["center"]
        self.ly = STICK_RANGE["center"]
        self.rx = STICK_RANGE["center"]
        self.ry = STICK_RANGE["center"]
        self.l_stick_changed = True
        self.r_stick_changed = True

    def reset_hat(self):
        self.hat = Hat.CENTER

    def reset(self):
        self.reset_buttons()
        self.reset_directions()

    def copy(self):
        return ControllerState(
            buttons=self.buttons,
            hat=self.hat,
            lx=self.lx,
            ly=self.ly,
            rx=self.rx,
            ry=self.ry,
            l_stick_changed=self.l_stick_changed,
            r_stick_changed=self.r_stick_changed,
        )


class ControllerStateSerializer:
    @staticmethod
    def serialize(controller_state: ControllerState) -> str:
        str_l = ""
        str_r = ""

        flag_buttons = int(controller_state.buttons) << 2
        if controller_state.l_stick_changed:
            flag_buttons |= 0x2
            str_l = f"{format(controller_state.lx, "x")} {format(controller_state.ly, "x")}"
        if controller_state.r_stick_changed:
            flag_buttons |= 0x1
            str_r = f"{format(controller_state.rx, "x")} {format(controller_state.ry, "x")}"
        str_hat = str(int(controller_state.hat))

        return f"{format(flag_buttons, "#06x")} {str_hat} {str_l} {str_r}"


class Controller:
    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__state = ControllerState()
        self.__serial = Serial(logger=logger)

    def open(self, port: str):
        self.__serial.open(port=port)

    def one_shot_buttons(self, buttons: list[Button], duration=0.1):
        self.hold_buttons(buttons)
        self.wait(duration)
        self.release_buttons(buttons)

    def hold_buttons(self, buttons: list[Button]):
        self.__state.set(buttons=buttons)
        self.__send_state()

    def release_buttons(self, buttons: list[Button]):
        self.__state.unset(buttons=buttons)
        self.__send_state()

    def __send_state(self):
        state = ControllerStateSerializer.serialize(self.__state)
        self.__serial.write_line(state)

    @staticmethod
    def wait(wait):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
