from switchpokepilot.config import _init_config

config = _init_config()


def reload_config():
    global config
    config = _init_config()
