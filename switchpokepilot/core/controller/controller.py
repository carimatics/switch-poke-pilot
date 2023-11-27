import time
from time import sleep
from typing import Optional

from switchpokepilot.core.controller.button import Button
from switchpokepilot.core.controller.hat import Hat
from switchpokepilot.core.controller.state import ControllerState
from switchpokepilot.core.controller.state_serializer import ControllerStateSerializer
from switchpokepilot.core.controller.stick import StickDisplacement
from switchpokepilot.core.libs.serial import SerialPort, SerialPortInfo


class Controller:
    def __init__(self):
        self._state = ControllerState()
        self._serial = SerialPort()

    @property
    def is_open(self) -> bool:
        return self._serial.is_open

    def open(self, port_info: SerialPortInfo):
        self._serial.open(port_info, baud_rate=9600)

    def close(self):
        self._serial.close()

    def set_state(self, state: ControllerState):
        self._state = state

    def set(self,
            buttons: Optional[list[Button]] = None,
            l_displacement: Optional[StickDisplacement] = None,
            r_displacement: Optional[StickDisplacement] = None,
            hat: Optional[Hat] = None):
        self._state.set(buttons=buttons,
                        l_displacement=l_displacement,
                        r_displacement=r_displacement,
                        hat=hat)

    def unset(self,
              buttons: Optional[list[Button]] = None,
              hat: bool = False):
        self._state.unset(buttons=buttons,
                          hat=hat)

    def reset(self):
        self._state.reset()

    def send(self):
        state_line = ControllerStateSerializer.serialize(self._state)
        self._serial.write_line(state_line)
        self._state.consume_stick_displacement()

    def send_hold(self,
                  buttons: Optional[list[Button]] = None,
                  l_displacement: Optional[StickDisplacement] = None,
                  r_displacement: Optional[StickDisplacement] = None,
                  hat: Optional[Hat] = None):
        self.set(buttons=buttons,
                 l_displacement=l_displacement,
                 r_displacement=r_displacement,
                 hat=hat)
        self.send()

    def send_reset(self):
        self.reset()
        self.send()

    def send_one_shot(self,
                      buttons: Optional[list[Button]] = None,
                      l_displacement: Optional[StickDisplacement] = None,
                      r_displacement: Optional[StickDisplacement] = None,
                      hat: Optional[Hat] = None,
                      duration=0.1):
        self.send_hold(buttons=buttons,
                       l_displacement=l_displacement,
                       r_displacement=r_displacement,
                       hat=hat)
        self._wait(duration)
        self.send_reset()

    def send_repeat(self,
                    times: int = 1,
                    buttons: Optional[list[Button]] = None,
                    l_displacement: Optional[StickDisplacement] = None,
                    r_displacement: Optional[StickDisplacement] = None,
                    hat: Optional[Hat] = None,
                    duration: float = 0.1,
                    interval: float = 0.1,
                    skip_last_interval: bool = True):
        if times < 1:
            return

        for i in range(times):
            self.send_one_shot(buttons=buttons,
                               l_displacement=l_displacement,
                               r_displacement=r_displacement,
                               hat=hat,
                               duration=duration)

            if skip_last_interval and i >= times - 1:
                break

            self._wait(interval)

    @staticmethod
    def _wait(wait: float):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
