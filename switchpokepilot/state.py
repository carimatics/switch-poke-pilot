from abc import ABCMeta, abstractmethod

from switchpokepilot.camera import Camera
from switchpokepilot.commands.command import Command
from switchpokepilot.controller.controller import Controller
from switchpokepilot.logger import AppLogger


class AppStateObserver(metaclass=ABCMeta):
    @abstractmethod
    def on_app_state_update(self, subject) -> None:
        raise NotImplementedError


class AppState:
    def __init__(self):
        self.__camera: Camera | None = None
        self.__capture_size: tuple[int, int] = (1280, 720)
        self.__observers: list[AppStateObserver] = []
        self.__logger: AppLogger = AppLogger()
        self.__controller: Controller = Controller(logger=self.__logger)
        self.__command: Command | None = None

    @property
    def camera(self) -> Camera:
        return self.__camera

    @camera.setter
    def camera(self, new_value: Camera):
        self.__camera = new_value
        self.__notify_observers()

    @property
    def capture_size(self) -> tuple[int, int]:
        return self.__capture_size

    @capture_size.setter
    def capture_size(self, new_value: tuple[int, int]):
        self.__capture_size = new_value

    @property
    def logger(self):
        return self.__logger

    @property
    def controller(self):
        return self.__controller

    @property
    def command(self):
        return self.__command

    @command.setter
    def command(self, new_value):
        self.__command = new_value
        self.__notify_observers()

    def reset_camera(self):
        self.__camera = Camera(capture_size=self.capture_size)
        self.__notify_observers()

    def __notify_observers(self):
        for observer in self.__observers:
            observer.on_app_state_update(self)

    def add_observer(self, observer: AppStateObserver):
        self.__observers.append(observer)

    def delete_observer(self, observer: AppStateObserver):
        try:
            self.__observers.remove(observer)
        finally:
            pass
