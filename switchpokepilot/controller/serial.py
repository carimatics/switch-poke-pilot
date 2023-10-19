import time

import serial

from switchpokepilot.exceptions import NotSupportedOS
from switchpokepilot.logger import Logger
from switchpokepilot.utils.os import is_macos, is_windows, is_linux


class Serial:
    def __init__(self, logger: Logger):
        self._logger = logger
        self._serial: serial.Serial | None = None

        self._content_last_wrote: str | None = None
        self._time_before_write: float | None = None
        self._time_after_write: float | None = None

    def open(self, port: str, name: str = "", baud_rate: int = 9600):
        try:
            if name is None or name == "":
                name = self._determine_name(port)

            self._logger.debug(f"connecting to {name}")
            self._serial = serial.Serial(name, baud_rate)
            return True
        except NotSupportedOS as e:
            self._logger.error("COM Port: not supported OS.")
            self._logger.error(f"{e}")
            return False
        except IOError as e:
            self._logger.error("COM Port: can't be established.")
            self._logger.error(f"{e}")
            return False

    def close(self):
        self._logger.debug("Closing the serial communication.")
        self._serial.close()
        self._serial = None

    def is_open(self):
        return self._serial is not None and self._serial.isOpen()

    def write_line(self, line: str):
        try:
            self._serial.write(f"{line}\r\n".encode("utf-8"))
        except serial.SerialException as e:
            self._logger.error(f"{e}")
        except AttributeError as e:
            self._logger.error("Maybe using a port that is not open.")
            self._logger.error(f"{e}")

    def write_line_with_perf_counter(self, line: str):
        self._time_before_write = time.perf_counter()
        self.write_line(line)
        self._time_after_write = time.perf_counter()
        self._content_last_wrote = line

    @staticmethod
    def _determine_name(port: str) -> str:
        if is_windows():
            return f"COM{port}"
        elif is_macos():
            return f"/dev/tty.usbserial-{port}"
        elif is_linux():
            return f"/dev/ttyUSB{port}"
        else:
            raise NotSupportedOS
