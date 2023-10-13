import os


def is_windows() -> bool:
    return os.name == 'nt'
