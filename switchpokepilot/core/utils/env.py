import sys


def is_packed() -> bool:
    # PyInstaller Run-time Information
    # See https://pyinstaller.org/en/stable/runtime-information.html#run-time-information
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
