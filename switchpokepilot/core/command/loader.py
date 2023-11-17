import importlib.util
import os
from typing import Type, Any

from switchpokepilot.core.config.config import Config
from switchpokepilot.core.path.path import Path


class CommandLoader:
    def __init__(self, config: Config, path: Path):
        self._config = config
        self._path = path

    def load(self, name: str) -> Type[Any]:
        return self._get_class(name)

    def get_names(self) -> list[str]:
        return [name for name in os.listdir(self._path.commands())
                if not name.startswith('.')]

    def get_info(self):
        return [{
            'name': name,
            'config': self._config.read_command_config(name)
        } for name in self.get_names()]

    def _get_class(self, name: str) -> Type[Any]:
        spec = importlib.util.spec_from_file_location('command', f"{self._path.command(name)}/command.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Command
