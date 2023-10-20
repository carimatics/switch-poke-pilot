import os.path

from switchpokepilot.config import config
from switchpokepilot.core.utils.env import is_packed

ASSETS_DIR = {
    "packed": os.path.join("assets"),
    "unpacked": os.path.join("..", "assets"),
}
CAPTURES_DIR = {
    "packed": os.path.join("captures"),
    "unpacked": os.path.join("..", "captures")
}
TEMPLATES_DIR = "templates"
MASKS_DIR = "templates"


def get_assets_dir():
    if is_packed():
        assets_dir = ASSETS_DIR["packed"]
    else:
        assets_dir = ASSETS_DIR["unpacked"]
    return os.path.join(config["root_dir"], assets_dir)


def get_captures_dir():
    if is_packed():
        captures_dir = CAPTURES_DIR["packed"]
    else:
        captures_dir = CAPTURES_DIR["unpacked"]
    return os.path.join(config["root_dir"], captures_dir)


def get_templates_dir():
    return os.path.join(get_assets_dir(), TEMPLATES_DIR)


def get_masks_dir():
    return os.path.join(get_assets_dir(), MASKS_DIR)
