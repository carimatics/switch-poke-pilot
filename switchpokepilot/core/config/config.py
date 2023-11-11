import json
from os import path
from typing import Optional

_user_config_file_path = path.expanduser("~/SwitchPokePilot.config.json")


class Config:
    def read_command_config(self, name: str):
        return self.read(path.join("commands", name))

    def read(self, relative_path: Optional[str] = None):
        if relative_path is None:
            absolute_path = path.abspath(path.join(self.get_user_directory(), "config.json"))
        else:
            absolute_path = path.abspath(path.join(self.get_user_directory(), relative_path, "config.json"))
        return self._read_json_file(absolute_path)

    def get_user_directory(self):
        if not path.exists(_user_config_file_path):
            raise FileNotFoundError(f"User config file not found: {_user_config_file_path}")
        user_directory = self._read_json_file(_user_config_file_path)['userDirectory']
        return path.abspath(path.expanduser(user_directory))

    @staticmethod
    def _read_json_file(path_name: Optional[str]):
        if not path.exists(path_name):
            raise FileNotFoundError(f"Config file not found: {path_name}")
        with open(path_name) as config_file:
            return json.load(config_file)
