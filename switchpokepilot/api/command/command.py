from switchpokepilot.api.command.config import CommandConfigAPI
from switchpokepilot.api.command.controller import CommandControllerAPI
from switchpokepilot.api.command.extensions import CommandExtensionsAPI
from switchpokepilot.api.command.image import CommandImageAPI
from switchpokepilot.api.command.logger import CommandLoggerAPI
from switchpokepilot.api.command.timer import CommandTimerAPI
from switchpokepilot.api.command.video import CommandVideoAPI
from switchpokepilot.core.camera import Camera
from switchpokepilot.core.config.config import Config
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.logger.logger import Logger
from switchpokepilot.core.path.path import Path
from switchpokepilot.core.timer import Timer


class CommandAPI:
    def __init__(self,
                 name: str,
                 logger: Logger,
                 controller: Controller,
                 config: Config,
                 camera: Camera,
                 path: Path,
                 timer: Timer):
        self._name = name
        self._config = CommandConfigAPI(config=config, command=name)
        self._controller = CommandControllerAPI(controller=controller)
        self._video = CommandVideoAPI(camera=camera, path=path)
        self._image = CommandImageAPI(path=path, command=name)
        self._timer = CommandTimerAPI(timer=timer)
        self._logger = CommandLoggerAPI(logger=logger)
        self._extensions = CommandExtensionsAPI(camera=camera, path=path, controller=controller)

    @property
    def name(self):
        return self._name

    @property
    def config(self):
        return self._config

    @property
    def controller(self):
        return self._controller

    @property
    def video(self):
        return self._video

    @property
    def image(self):
        return self._image

    @property
    def logger(self):
        return self._logger

    @property
    def timer(self):
        return self._timer

    @property
    def extensions(self):
        return self._extensions
