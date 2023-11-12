from datetime import datetime
from os import path
from typing import Optional, Any

from switchpokepilot.core.config.config import Config


class Path:
    def __init__(self, config: Config):
        self._config = config

        self._user_directory = None
        self._user_config = None
        self._templates_path = None
        self._captures_path = None
        self._commands_path = None

    def user_directory(self, cache: bool = True) -> str:
        if cache and self._user_directory is not None:
            return self._user_directory
        else:
            self._user_directory = self._config.get_user_directory()
            return self._user_directory

    def user_config(self, cache: bool = True) -> Any:
        if cache and self._user_config is not None:
            return self._user_config
        else:
            self._user_config = self._config.read()
            return self._user_config

    def templates(self, cache: bool = True) -> str:
        if cache and self._templates_path is not None:
            return self._templates_path
        else:
            relational_path = self.user_config(cache=cache)["directories"]["templates"]
            self._templates_path = path.join(self.user_directory(cache=cache), relational_path)
            return self._templates_path

    def captures(self, cache: bool = True) -> str:
        if cache and self._captures_path is not None:
            return self._captures_path
        else:
            relational_path = self.user_config(cache=cache)["directories"]["captures"]
            self._captures_path = path.join(self.user_directory(cache=cache), relational_path)
            return self._captures_path

    def commands(self, cache: bool = True) -> str:
        if cache and self._commands_path is not None:
            return self._commands_path
        else:
            relational_path = self.user_config(cache=cache)["directories"]["commands"]
            self._commands_path = path.join(self.user_directory(cache=cache), relational_path)
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
    def _normalize_file_name(name: str | None = None) -> str:
        if name is None or name == "":
            now = datetime.now()
            return f"{now.strftime("%Y-%m-%d_%H-%M-%S-%f")}.png"

        if not name.endswith(".png"):
            return f"{name}.png"

        return name
