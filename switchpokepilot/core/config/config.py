import json
import os.path
from typing import Optional

from switchpokepilot.core.path.path import Path


class Config:
    def __init__(self, path: Path):
        self._path = path

    def read_command_config(self, name: str):
        return self.read(os.path.join("commands", name))

    def read(self, relative_path: Optional[str] = None):
        absolute_path = os.path.join(self._path.user_directory(), relative_path, "config.json")
        return self._read_json_file(absolute_path)

    @staticmethod
    def _read_json_file(path_name: Optional[str]):
        if not os.path.exists(path_name):
            raise FileNotFoundError(f"Config file not found: {path_name}")
        with open(path_name, encoding='utf-8') as config_file:
            return json.load(config_file)
