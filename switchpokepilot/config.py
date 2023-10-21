import sys
from configparser import ConfigParser
from os import path

from switchpokepilot.core.utils.env import is_packed

FILE_NAME = "config.ini"


def _get_runtime_root():
    if is_packed():
        return getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
    else:
        return "."


def _init_config():
    config = ConfigParser()
    file_path = path.abspath(path.join(_get_runtime_root(), FILE_NAME))
    config.read(file_path)
    return config
