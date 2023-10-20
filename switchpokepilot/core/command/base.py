from dataclasses import dataclass

from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.logger import Logger


@dataclass
class CommandInitParams:
    controller: Controller
    logger: Logger


class BaseCommand:
    def __init__(self, params: CommandInitParams):
        self.should_running: bool = False
        self.name: str = 'Command'
        self.controller = params.controller
        self.logger = params.logger

    def preprocess(self):
        self.should_running = True

    def process(self):
        raise NotImplementedError

    def postprocess(self):
        self.should_running = False
