import multiprocessing
from abc import abstractmethod, ABCMeta

from switch_pilot_core.camera import Camera
from switch_pilot_core.config import Config
from switch_pilot_core.controller import Controller
from switch_pilot_core.logger import Logger
from switch_pilot_core.path import Path

from switchpokepilot.mainwindow.logger import MainWindowLogger


class MainWindowStateObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_main_window_state_update(self, subject) -> None:
        raise NotImplementedError


class MainWindowState:
    def __init__(self, queue: multiprocessing.Queue):
        self._observers: list[MainWindowStateObserver] = []
        self._queue = queue

        self._logger: Logger = MainWindowLogger()
        self._path: Path = Path()
        self._config: Config = Config(path=self._path)

        self._camera: Camera = self._create_default_camera()

        self._controller: Controller = Controller()

    @property
    def logger(self):
        return self._logger

    @property
    def path(self):
        return self._path

    @property
    def config(self):
        return self._config

    @property
    def controller(self):
        return self._controller

    @property
    def camera(self):
        return self._camera

    @camera.setter
    def camera(self, new_value):
        current_camera = self._camera
        if current_camera is not None:
            current_camera.release()

        self._camera = new_value
        self._notify()

    def destruct(self):
        self._camera.release()
        self._controller.close()

    def add_observer(self, observer: MainWindowStateObserver):
        self._observers.append(observer)

    def remove_observer(self, observer: MainWindowStateObserver):
        try:
            self._observers.remove(observer)
        finally:
            pass

    def _notify(self):
        for observer in self._observers:
            observer.on_main_window_state_update(self)

    def _create_default_camera(self):
        camera = Camera(capture_size=(1280, 720),
                        logger=self._logger)
        devices = Camera.get_devices()
        if len(devices) > 0:
            camera.name = devices[0]["name"]
            camera.id = devices[0]["id"]
        return camera
