from abc import ABCMeta, abstractmethod

from switchpokepilot.core.camera import Camera
from switchpokepilot.core.command.base import BaseCommand
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.image.processor import ImageProcessor
from switchpokepilot.core.logger import AppLogger


class AppStateObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_app_state_update(self, subject) -> None:
        raise NotImplementedError


class AppState:
    def __init__(self):
        self._logger: AppLogger = AppLogger()
        self._observers: list[AppStateObserver] = []

        # for image processing
        self._capture_size: tuple[int, int] = (1280, 720)
        self._camera: Camera | None = None
        self._image_processor = ImageProcessor(logger=self._logger)

        # for manipulate game
        self._controller: Controller = Controller(logger=self._logger)
        self._command: BaseCommand | None = None

    @property
    def logger(self):
        return self._logger

    @property
    def capture_size(self) -> tuple[int, int]:
        return self._capture_size

    @capture_size.setter
    def capture_size(self, new_value: tuple[int, int]):
        self._capture_size = new_value

    @property
    def camera(self) -> Camera:
        return self._camera

    @camera.setter
    def camera(self, new_value: Camera):
        self._camera = new_value
        self._notify()

    @property
    def image_processor(self):
        return self._image_processor

    @property
    def controller(self):
        return self._controller

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, new_value):
        self._command = new_value
        self._notify()

    def _notify(self):
        for observer in self._observers:
            observer.on_app_state_update(self)

    def add_observer(self, observer: AppStateObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: AppStateObserver):
        try:
            self._observers.remove(observer)
        finally:
            pass
