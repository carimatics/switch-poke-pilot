import time

import serial

from switchpokepilot.exceptions import NotSupportedOS
from switchpokepilot.logger import Logger
from switchpokepilot.utils.os import is_macos, is_windows, is_linux


class Serial:
    def __init__(self, logger: Logger):
        self.__logger = logger
        self.__serial: serial.Serial | None = None

        self.__content_last_wrote: str | None = None
        self.__time_before_write: float | None = None
        self.__time_after_write: float | None = None

    def open(self, port: str, name: str = "", baud_rate: int = 9600):
        try:
            if name is None or name == "":
                name = self.__determine_name(port)

            self.__logger.debug(f"connecting to {name}")
            self.__serial = serial.Serial(name, baud_rate)
            return True
        except NotSupportedOS as e:
            self.__logger.error("COM Port: not supported OS.")
            self.__logger.error(f"{e}")
            return False
        except IOError as e:
            self.__logger.error("COM Port: can't be established.")
            self.__logger.error(f"{e}")
            return False

    def close(self):
        self.__logger.debug("Closing the serial communication.")
        self.__serial.close()
        self.__serial = None

    def is_open(self):
        return self.__serial is not None and self.__serial.isOpen()

    def write_line(self, line: str):
        try:
            self.__serial.write(f"{line}\r\n".encode("utf-8"))
        except serial.SerialException as e:
            self.__logger.error(f"{e}")
        except AttributeError as e:
            self.__logger.error("Maybe using a port that is not open.")
            self.__logger.error(f"{e}")

    def write_line_with_perf_counter(self, line: str):
        self.__time_before_write = time.perf_counter()
        self.write_line(line)
        self.__time_after_write = time.perf_counter()
        self.__content_last_wrote = line

    @staticmethod
    def __determine_name(port: str) -> str:
        if is_windows():
            return f"COM{port}"
        elif is_macos():
            return f"/dev/tty.usbserial-{port}"
        elif is_linux():
            return f"/dev/ttyUSB{port}"
        else:
            raise NotSupportedOS
