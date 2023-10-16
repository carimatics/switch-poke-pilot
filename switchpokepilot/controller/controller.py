import math
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


class StickTilt(Enum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class StickSide(Enum):
    RIGHT = auto()
    LEFT = auto()


STICK_DISPLACEMENT_RANGE = {
    "min": 0,
    "center": 128,
    "max": 255,
}


class StickDisplacement:
    def __init__(self, angle: float, magnification: float = 1.0):
        self.magnification = self.__clamp_magnification(magnification)
        if magnification == 0.0:
            center = STICK_DISPLACEMENT_RANGE["center"]
            self.x, self.y = center, center
        else:
            self.x, self.y = self.__calculate_xy(angle, magnification)
        self.tilts = self.__calculate_tilts(self.x, self.y)

    @staticmethod
    def __clamp_magnification(magnification: float):
        if magnification < 0.0:
            return 0.0
        elif magnification > 1.0:
            return 1.0
        else:
            return magnification

    @staticmethod
    def __calculate_xy(angle: float, magnification: float) -> tuple[int, int]:
        rad = math.radians(angle)
        x = math.ceil(127.5 * math.cos(rad) * magnification + 127.5)
        y = math.floor(127.5 * math.sin(rad) * magnification + 127.5)
        return x, y

    @staticmethod
    def __calculate_tilts(x: int, y: int) -> list[StickTilt]:
        center = STICK_DISPLACEMENT_RANGE["center"]
        tilts = []
        if x < center:
            tilts.append(StickTilt.LEFT)
        elif x > center:
            tilts.append(StickTilt.RIGHT)
        if y < center - 1:
            tilts.append(StickTilt.DOWN)
        elif y > center - 1:
            tilts.append(StickTilt.UP)
        return tilts


class StickDisplacementPreset:
    CENTER = StickDisplacement(angle=0, magnification=0.0)
    UP_LEFT = StickDisplacement(angle=135)
    UP = StickDisplacement(angle=90)
    UP_RIGHT = StickDisplacement(angle=45)
    RIGHT = StickDisplacement(angle=0)
    DOWN_LIGHT = StickDisplacement(angle=-45)
    DOWN = StickDisplacement(angle=-90)
    DOWN_LEFT = StickDisplacement(angle=-135)
    LEFT = StickDisplacement(angle=-180)


class Stick:
    def __init__(self,
                 side: StickSide,
                 displacement: StickDisplacement | None = None):
        self.side = side
        if displacement is None:
            self.x, self.y = 0, 0
        else:
            self.set_displacement(displacement)
        self.changed = False

    def consume(self):
        self.changed = False

    def set_displacement(self, displacement: StickDisplacement):
        if self.x != displacement.x or self.y != displacement.y:
            self.changed = True
            self.x, self.y = displacement.x, 255 - displacement.y

    def reset(self):
        center = STICK_DISPLACEMENT_RANGE["center"]
        if self.x != center or self.y != center:
            self.x, self.y = center, center
            self.changed = True

    def unset_tilt(self, tilts: list[StickTilt] | None = None):
        if tilts is None:
            return

        center = STICK_DISPLACEMENT_RANGE["center"]
        if StickTilt.UP in tilts or StickTilt.DOWN in tilts:
            self.y = center
            self.x = self.__extreme_tilt(self.x)
            self.changed = True
        if StickTilt.LEFT in tilts or StickTilt.RIGHT in tilts:
            self.x = center
            self.y = self.__extreme_tilt(self.y)
            self.changed = True

    @staticmethod
    def __extreme_tilt(displacement: int) -> int:
        center = STICK_DISPLACEMENT_RANGE["center"]
        if displacement > center:
            return STICK_DISPLACEMENT_RANGE["max"]
        if displacement < center:
            return STICK_DISPLACEMENT_RANGE["min"]
        return center


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
        self.l_stick = Stick(side=StickSide.LEFT)
        self.l_stick.x = lx
        self.l_stick.y = ly
        self.l_stick.changed = l_stick_changed

        # R stick
        self.r_stick = Stick(side=StickSide.RIGHT)
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

    def unset_stick_tilt(self,
                         l_tilts: list[StickTilt] | None = None,
                         r_tilts: list[StickTilt] | None = None):
        if l_tilts is not None:
            self.l_stick.unset_tilt(tilts=l_tilts)
        if r_tilts is not None:
            self.r_stick.unset_tilt(tilts=r_tilts)

    def reset_buttons(self):
        self.buttons = 0

    def reset_stick_displacement(self):
        self.l_stick.reset()
        self.r_stick.reset()

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


class Controller:
    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__state = ControllerState()
        self.__serial = Serial(logger=logger)

    def open(self, port: str):
        self.__serial.open(port=port)

    def close(self):
        self.__serial.close()

    def set(self,
            buttons: list[Button] | None = None,
            l_displacement: StickDisplacement | None = None,
            r_displacement: StickDisplacement | None = None,
            hat: Hat | None = None):
        self.__state.set(buttons=buttons,
                         l_displacement=l_displacement,
                         r_displacement=r_displacement,
                         hat=hat)

    def reset(self):
        self.__state.reset()

    def send(self):
        state_line = ControllerStateSerializer.serialize(self.__state)
        self.__serial.write_line(state_line)

    def neutral_stick(self):
        self.__state.reset_stick_displacement()

    def send_hold(self,
                  buttons: list[Button] | None = None,
                  l_displacement: StickDisplacement | None = None,
                  r_displacement: StickDisplacement | None = None,
                  hat: Hat | None = None):
        self.set(buttons=buttons,
                 l_displacement=l_displacement,
                 r_displacement=r_displacement,
                 hat=hat)
        self.send()

    def send_reset(self):
        self.reset()
        self.send()

    def send_one_shot(self,
                      buttons: list[Button] | None = None,
                      l_displacement: StickDisplacement | None = None,
                      r_displacement: StickDisplacement | None = None,
                      hat: Hat | None = None,
                      duration=0.1):
        self.send_hold(buttons=buttons,
                       l_displacement=l_displacement,
                       r_displacement=r_displacement,
                       hat=hat)
        self.wait(duration)
        self.send_reset()

    def send_repeat(self,
                    count: int = 1,
                    buttons: list[Button] | None = None,
                    l_displacement: StickDisplacement | None = None,
                    r_displacement: StickDisplacement | None = None,
                    hat: Hat | None = None,
                    duration: float = 0.1,
                    interval: float = 0.1,
                    skip_last_interval: bool = True):
        if count < 1:
            return

        for i in range(count):
            self.send_one_shot(buttons=buttons,
                               l_displacement=l_displacement,
                               r_displacement=r_displacement,
                               hat=hat,
                               duration=duration)
            if skip_last_interval and i + 1 < count:
                self.wait(interval)

    @staticmethod
    def wait(wait: float):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
