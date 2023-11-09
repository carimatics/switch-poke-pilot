import time
from time import sleep

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

    def open(self, port_info: SerialPortInfo):
        self._serial.open(port_info, baud_rate=9600)

    def close(self):
        self._serial.close()

    def set(self,
            buttons: list[Button] | None = None,
            l_displacement: StickDisplacement | None = None,
            r_displacement: StickDisplacement | None = None,
            hat: Hat | None = None):
        self._state.set(buttons=buttons,
                        l_displacement=l_displacement,
                        r_displacement=r_displacement,
                        hat=hat)

    def reset(self):
        self._state.reset()

    def send(self):
        state_line = ControllerStateSerializer.serialize(self._state)
        self._serial.write_line(state_line)

    def neutral_stick(self):
        self._state.reset_stick_displacement()

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

            if skip_last_interval and i >= count - 1:
                break

            self.wait(interval)

    @staticmethod
    def wait(wait: float):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = time.perf_counter()
            while time.perf_counter() < current_time + wait:
                pass
