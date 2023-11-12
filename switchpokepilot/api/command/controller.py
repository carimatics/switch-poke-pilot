from typing import Optional

from switchpokepilot.app.ui.button import Button
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.controller.hat import Hat
from switchpokepilot.core.controller.stick import StickDisplacement, StickDisplacementPreset


class CommandControllerStickAPI:
    @property
    def presets(self):
        return StickDisplacementPreset

    @staticmethod
    def create(angle: float, magnification: float):
        return StickDisplacement(angle=angle, magnification=magnification)


class CommandControllerAPI:
    def __init__(self, controller: Controller):
        self._controller = controller

        # stick
        self._stick_api = CommandControllerStickAPI()
        self._stick = self._stick_api.presets
        self._stick.create = self._stick_api.create

    @property
    def button(self):
        return Button

    @property
    def hat(self):
        return Hat

    @property
    def stick(self):
        return self._stick

    def set(self,
            buttons: Optional[list[Button]] = None,
            l_stick: Optional[StickDisplacement] = None,
            r_stick: Optional[StickDisplacement] = None,
            hat: Optional[Hat] = None):
        self._controller.set(buttons=buttons,
                             l_displacement=l_stick,
                             r_displacement=r_stick,
                             hat=hat)

    def reset(self):
        self._controller.reset()

    def send(self):
        self._controller.send()

    def send_hold(self,
                  buttons: Optional[list[Button]] = None,
                  l_stick: Optional[StickDisplacement] = None,
                  r_stick: Optional[StickDisplacement] = None,
                  hat: Optional[Hat] = None):
        self._controller.send_hold(buttons=buttons,
                                   l_displacement=l_stick,
                                   r_displacement=r_stick,
                                   hat=hat)

    def send_reset(self):
        self._controller.send_reset()

    def send_one_shot(self,
                      buttons: Optional[list[Button]] = None,
                      l_stick: Optional[StickDisplacement] = None,
                      r_stick: Optional[StickDisplacement] = None,
                      hat: Optional[Hat] = None,
                      duration: Optional[float] = None):
        self._controller.send_one_shot(buttons=buttons,
                                       l_displacement=l_stick,
                                       r_displacement=r_stick,
                                       hat=hat,
                                       duration=duration)

    def send_repeat(self,
                    buttons: Optional[list[Button]] = None,
                    l_stick: Optional[StickDisplacement] = None,
                    r_stick: Optional[StickDisplacement] = None,
                    hat: Optional[Hat] = None,
                    times: Optional[int] = None,
                    interval: Optional[float] = None,
                    duration: Optional[float] = None,
                    skip_last_interval: Optional[bool] = None):
        self._controller.send_repeat(buttons=buttons,
                                     l_displacement=l_stick,
                                     r_displacement=r_stick,
                                     hat=hat,
                                     times=times,
                                     interval=interval,
                                     duration=duration,
                                     skip_last_interval=skip_last_interval)
