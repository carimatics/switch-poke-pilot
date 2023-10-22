from dataclasses import dataclass

from switchpokepilot import reload_config
from switchpokepilot.core.camera import Camera
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.logger import Logger


@dataclass
class CommandInitParams:
    controller: Controller
    logger: Logger
    camera: Camera


class Command:
    NAME = "Command"

    def __init__(self, params: CommandInitParams):
        # basic information
        self.generation: str = "General"

        # running state
        self.should_keep_running: bool = False
        self.is_alive: bool = False

        self.controller = params.controller
        self.logger = params.logger
        self.camera = params.camera

    def preprocess(self):
        reload_config()
        self.should_keep_running = True
        self.is_alive = True

    def process(self):
        raise NotImplementedError

    def postprocess(self):
        self.should_keep_running = False
        self.is_alive = False

    def stop(self):
        self.should_keep_running = False

    def finish(self):
        self.should_keep_running = False
        self.is_alive = False
