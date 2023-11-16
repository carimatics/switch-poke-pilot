import json
import sys
from os import path
from typing import Optional

from switchpokepilot.core.utils.env import is_packed
from switchpokepilot.core.utils.os import is_macos


class Config:
    def read_command_config(self, name: str):
        return self.read(path.join("commands", name))

    def read(self, relative_path: Optional[str] = None):
        absolute_path = path.join(self.get_user_directory(), relative_path, "config.json")
        return self._read_json_file(absolute_path)

    @staticmethod
    def get_user_directory():
        if is_packed():
            if is_macos():
                return path.abspath(path.join(sys.executable, "..", "..", "..", "..", "SwitchPokePilot"))
            else:
                return path.join(path.dirname(sys.executable), "SwitchPokePilot")
        else:
            return path.abspath(
                path.join(path.abspath(__file__), "..", "..", "..", "..", "examples", "SwitchPokePilot"))

    @staticmethod
    def _read_json_file(path_name: Optional[str]):
        if not path.exists(path_name):
            raise FileNotFoundError(f"Config file not found: {path_name}")
        with open(path_name, encoding='utf-8') as config_file:
            return json.load(config_file)
