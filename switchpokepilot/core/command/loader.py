import importlib.util
import os
from typing import Type

from switchpokepilot.core.command.base import BaseCommand


class CommandLoader:
    def __init__(self, dir_name: str):
        self.dir_name = dir_name

    def load(self) -> list[Type[BaseCommand]]:
        names = [name for name in self._get_file_names() if not name.startswith("__")]
        return [self._get_class(name) for name in names]

    def _get_file_names(self) -> list[str]:
        return os.listdir(os.path.abspath(self.dir_name))

    def _get_class(self, name: str) -> Type[BaseCommand]:
        spec = importlib.util.spec_from_file_location(name, f"{self.dir_name}/{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Command
