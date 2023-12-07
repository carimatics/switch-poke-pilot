from abc import ABCMeta, abstractmethod

from switch_pilot_core.camera import Camera
from switch_pilot_core.command import CommandRunner
from switch_pilot_core.config import Config
from switch_pilot_core.controller import Controller
from switch_pilot_core.path import Path

from switchpokepilot.logger import AppLogger


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

        # for manipulate game
        self._controller: Controller = Controller()
        self._command_runner: CommandRunner = CommandRunner()

        self._path = Path()
        self._config = Config(self._path)

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
        current_camera = self._camera
        if current_camera is not None:
            current_camera.release()

        self._camera = new_value
        self._notify()

    @property
    def controller(self):
        return self._controller

    @property
    def command_runner(self):
        return self._command_runner

    @property
    def config(self):
        return self._config

    @property
    def path(self):
        return self._path

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
