from typing import Type

from .hunt_ursaluna_bloodmoon import HuntUrsalunaBloodmoon
from .mash_a import MashA
from ..base import Command

command_classes: list[Type[Command]] = [
    MashA,
    HuntUrsalunaBloodmoon,
]
