import sys
from enum import StrEnum, auto
from os import path

from switchpokepilot import config
from switchpokepilot.core.utils.env import is_packed

ASSETS_SECTION_KEY = "assets"
CAPTURES_SECTION_KEY = "captures"


class DirectoryNotSupportedError(Exception):
    pass


class DirectoryKind(StrEnum):
    RUNTIME_ROOT = auto()
    ASSETS = auto()
    TEMPLATES = auto()
    MASKS = auto()
    CAPTURES = auto()


def _get_runtime_root_dir():
    if is_packed():
        root_dir = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
    else:
        root_dir = "."

    return path.abspath(root_dir)


def _get_assets_base_dir():
    base_dir = config[ASSETS_SECTION_KEY]["BaseDir"]

    if base_dir == "::embedded::":
        return _get_runtime_root_dir()

    if base_dir.startswith("~"):
        return path.expanduser(base_dir)

    if path.isabs(base_dir):
        return base_dir

    raise DirectoryNotSupportedError


def _get_captures_dir():
    captures_dir = config[CAPTURES_SECTION_KEY]["CapturesDir"]

    if captures_dir.startswith("~"):
        return path.expanduser(captures_dir)

    if path.isabs(captures_dir):
        return captures_dir

    raise DirectoryNotSupportedError


def _get_asset_dir(kind: DirectoryKind):
    if kind == DirectoryKind.ASSETS:
        key = "AssetsDir"
    elif kind == DirectoryKind.TEMPLATES:
        key = "TemplatesDir"
    elif kind == DirectoryKind.MASKS:
        key = "MasksDir"
    else:
        return DirectoryNotSupportedError

    base_dir = _get_assets_base_dir()
    sub_path = config[ASSETS_SECTION_KEY][key]
    return path.abspath(path.join(base_dir, sub_path))


def get_dir(kind: DirectoryKind):
    if kind == DirectoryKind.RUNTIME_ROOT:
        return _get_runtime_root_dir()
    elif kind == DirectoryKind.CAPTURES:
        return _get_captures_dir()
    elif kind == DirectoryKind.ASSETS:
        return _get_asset_dir(kind)
    elif kind == DirectoryKind.TEMPLATES:
        return _get_asset_dir(kind)
    elif kind == DirectoryKind.MASKS:
        return _get_asset_dir(kind)
    else:
        raise DirectoryNotSupportedError
