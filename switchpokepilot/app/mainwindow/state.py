import multiprocessing
from abc import abstractmethod, ABCMeta
from typing import Optional

from switchpokepilot.app.logger import AppLogger
from switchpokepilot.core.camera import Camera
from switchpokepilot.core.logger.logger import Logger


class MainWindowStateObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_main_window_state_update(self, subject) -> None:
        raise NotImplementedError


class MainWindowState:
    def __init__(self, queue: multiprocessing.Queue):
        self._observers: list[MainWindowStateObserver] = []
        self._queue = queue

        self._logger: Logger = AppLogger()
        self._camera: Optional[Camera] = None

    @property
    def logger(self):
        return self._logger

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, new_value):
        current_camera = self._camera
        if current_camera is not None:
            current_camera.destroy()

        self._camera = new_value
        self._notify()

    def _notify(self):
        for observer in self._observers:
            observer.on_main_window_state_update(self)

    def add_observer(self, observer: MainWindowStateObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: MainWindowStateObserver):
        try:
            self._observers.remove(observer)
        finally:
            pass
