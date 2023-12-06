from abc import ABCMeta, abstractmethod

from switch_pilot_core.logger.logger import Logger


class LoggerObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_log(self, message: str):
        raise NotImplementedError


class AppLogger(Logger):
    def __init__(self):
        self._observers: list[LoggerObserver] = []
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

    def add_observer(self, observer: LoggerObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: LoggerObserver):
        try:
            self._observers.remove(observer)
        finally:
            pass
