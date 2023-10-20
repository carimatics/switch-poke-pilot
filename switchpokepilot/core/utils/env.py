import os


def is_packed() -> bool:
    packed = os.environ.get("SWITCH_POKE_PILOT_PACKED", "true")
    return packed == "true"
