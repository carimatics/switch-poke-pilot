from dataclasses import dataclass

from switchpokepilot.core.camera import Camera
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.logger import Logger


@dataclass
class CommandInitParams:
    controller: Controller
    logger: Logger
    camera: Camera


class BaseCommand:
    NAME = "Command"

    def __init__(self, params: CommandInitParams):
        self.should_keep_running: bool = False
        self.generation: str = "General"
        self.controller = params.controller
        self.logger = params.logger
        self.camera = params.camera

    def preprocess(self):
        self.should_keep_running = True

    def process(self):
        raise NotImplementedError

    def postprocess(self):
        self.should_keep_running = False
