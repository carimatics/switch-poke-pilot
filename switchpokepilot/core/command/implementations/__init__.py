from typing import Type

from .mash_a import MashA
from ..base import Command

command_classes: list[Type[Command]] = [
    MashA,
]
