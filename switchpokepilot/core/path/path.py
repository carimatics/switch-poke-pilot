import sys
from datetime import datetime
from os import path
from typing import Optional

from switchpokepilot.core.utils.env import is_packed
from switchpokepilot.core.utils.os import is_macos


class Path:
    def __init__(self):
        self._user_directory: Optional[str] = None
        self._templates_path: Optional[str] = None
        self._captures_path: Optional[str] = None
        self._commands_path: Optional[str] = None

    def user_directory(self, cache: bool = True) -> str:
        if cache and self._user_directory is not None:
            return self._user_directory
        else:
            self._user_directory = self._get_user_directory()
            return self._user_directory

    def templates(self, cache: bool = True) -> str:
        if cache and self._templates_path is not None:
            return self._templates_path
        else:
            self._templates_path = path.join(self.user_directory(cache=cache), "templates")
            return self._templates_path

    def captures(self, cache: bool = True) -> str:
        if cache and self._captures_path is not None:
            return self._captures_path
        else:
            self._captures_path = path.join(self.user_directory(cache=cache), "captures")
            return self._captures_path

    def commands(self, cache: bool = True) -> str:
        if cache and self._commands_path is not None:
            return self._commands_path
        else:
            self._commands_path = path.join(self.user_directory(cache=cache), "commands")
            return self._commands_path

    def command(self, name: str, cache: bool = True) -> str:
        return path.join(self.commands(cache=cache), name)

    def template(self, name: str, command: Optional[str] = None, cache: bool = True) -> str:
        if command is None:
            return path.join(self.templates(cache=cache), name)
        else:
            return path.join(self.command(name=command, cache=cache), "templates", name)

    def capture(self, name: Optional[str] = None, cache: bool = True) -> str:
        normalized = self._normalize_file_name(name)
        return path.join(self.captures(cache=cache), normalized)

    @staticmethod
    def _get_user_directory():
        if is_packed():
            if is_macos():
                return path.abspath(path.join(sys.executable, "..", "..", "..", "..", "SwitchPokePilot"))
            else:
                return path.join(path.dirname(sys.executable), "SwitchPokePilot")
        else:
            return path.abspath(
                path.join(path.abspath(__file__), "..", "..", "..", "..", "examples", "SwitchPokePilot"))

    @staticmethod
    def _normalize_file_name(name: Optional[str] = None) -> str:
        if name is None or name == "":
            now = datetime.now()
            return f"{now.strftime("%Y-%m-%d_%H-%M-%S-%f")}.png"

        if not name.endswith(".png"):
            return f"{name}.png"

        return name
