import sys
from configparser import ConfigParser
from os import path

from switchpokepilot.core.utils.env import is_packed

FILE_NAME = "config.ini"
USER_CONFIG_PATH = f"~/Documents/SwitchPokePilot/{FILE_NAME}"


def _get_runtime_root():
    if is_packed():
        return getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
    else:
        return "."


def _init_config():
    config = ConfigParser()
    default_config = path.abspath(path.join(_get_runtime_root(), FILE_NAME))
    user_config = path.expanduser(USER_CONFIG_PATH)
    # Extend default config by user config if exists
    config.read([default_config, user_config])
    return config
