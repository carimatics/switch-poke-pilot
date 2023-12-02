from abc import ABCMeta, abstractmethod

from switchpokepilot.core.logger.logger import Logger


class MainWindowLoggerObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_log(self, message: str):
        raise NotImplementedError


class MainWindowLogger(Logger):
    def __init__(self):
        self._observers: list[MainWindowLoggerObserver] = []
        self.disabled: bool = False

    def debug(self, message):
        if self.disabled:
            return

        for observer in self._observers:
            observer.on_log(f"[DEBUG] {message}")

    def info(self, message):
        if self.disabled:
            return

        for observer in self._observers:
            observer.on_log(f"[INFO ] {message}")

    def warn(self, message):
        if self.disabled:
            return

        for observer in self._observers:
            observer.on_log(f"[WARN ] {message}")

    def error(self, message):
        if self.disabled:
            return

        for observer in self._observers:
            observer.on_log(f"[ERROR] {message}")

    def add_observer(self, observer: MainWindowLoggerObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: MainWindowLoggerObserver):
        try:
            self._observers.remove(observer)
        finally:
            pass
