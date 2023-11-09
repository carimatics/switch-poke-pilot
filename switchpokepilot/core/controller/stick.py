import math

STICK_DISPLACEMENT_RANGE = {
    "min": 0,
    "center": 128,
    "max": 255,
}


class StickDisplacement:
    def __init__(self, angle: float, magnification: float = 1.0):
        self.magnification = self._clamp_magnification(magnification)
        if self.magnification == 0.0:
            center = STICK_DISPLACEMENT_RANGE["center"]
            self.x, self.y = center, center
        else:
            self.x, self.y = self._calculate_xy(self._clamp_angle(angle), self.magnification)

    @staticmethod
    def _clamp_angle(angle: float) -> float:
        return angle % 360

    @staticmethod
    def _clamp_magnification(magnification: float):
        if magnification < 0.0:
            return 0.0
        elif magnification > 1.0:
            return 1.0
        else:
            return magnification

    @staticmethod
    def _calculate_xy(angle: float, magnification: float) -> tuple[int, int]:
        max_range = STICK_DISPLACEMENT_RANGE["max"]
        rad = math.radians(angle)
        x = math.ceil(127.5 * math.cos(rad) * magnification + 127.5)
        y = max_range - math.floor(127.5 * math.sin(rad) * magnification + 127.5)
        return x, y


class Stick:
    def __init__(self,
                 displacement: StickDisplacement | None = None):
        if displacement is None:
            center = STICK_DISPLACEMENT_RANGE["center"]
            self.x, self.y = center, center
        else:
            self.set_displacement(displacement)
        self.changed = False

    def consume(self):
        self.changed = False

    def set_displacement(self, displacement: StickDisplacement):
        if self.x != displacement.x or self.y != displacement.y:
            self.x, self.y = displacement.x, displacement.y
            self.changed = True

    def reset(self):
        center = STICK_DISPLACEMENT_RANGE["center"]
        if self.x != center or self.y != center:
            self.x, self.y = center, center
            self.changed = True

    @staticmethod
    def _extreme_tilt(displacement: int) -> int:
        center = STICK_DISPLACEMENT_RANGE["center"]
        if displacement > center:
            return STICK_DISPLACEMENT_RANGE["max"]
        if displacement < center:
            return STICK_DISPLACEMENT_RANGE["min"]
        return center


class StickDisplacementPreset:
    CENTER = StickDisplacement(angle=0, magnification=0.0)
    RIGHT = StickDisplacement(angle=0)
    TOP_RIGHT = StickDisplacement(angle=45)
    TOP = StickDisplacement(angle=90)
    TOP_LEFT = StickDisplacement(angle=135)
    LEFT = StickDisplacement(angle=180)
    BOTTOM_LEFT = StickDisplacement(angle=215)
    BOTTOM = StickDisplacement(angle=270)
    BOTTOM_RIGHT = StickDisplacement(angle=315)
