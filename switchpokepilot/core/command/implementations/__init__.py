from typing import Type

from .mash_a import MashA
from ..base import BaseCommand

command_classes: list[Type[BaseCommand]] = [
    MashA,
]
