from typing import Optional

import serial
import serial.tools.list_ports
from pydantic import BaseModel


class SerialPortInfo(BaseModel):
    path: str
    name: str


class SerialPort:
    def __init__(self):
        self._serial: Optional[serial.Serial] = None

    @property
    def is_open(self) -> bool:
        return self._serial is not None and self._serial.is_open

    @staticmethod
    def get_serial_ports() -> list[SerialPortInfo]:
        return [
            SerialPortInfo(path=port.device, name=port.name)
            for port in serial.tools.list_ports.comports()
            if port.description != "n/a"
        ]

    def close(self):
        self._serial.close()

    def open(self, info: SerialPortInfo, baud_rate: int):
        if self.is_open:
            self.close()
        self._serial = serial.Serial(port=info.path, baudrate=baud_rate)

    def write(self, content: str):
        if not self.is_open:
            raise Exception("SerialPort is not open.")

        self._serial.write(content.encode('utf-8'))

    def write_line(self, line: str):
        self.write(f"{line}\r\n")
