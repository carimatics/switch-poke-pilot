from dataclasses import dataclass
from time import sleep, perf_counter

from switchpokepilot.core.camera import Camera
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.image.processor import ImageProcessor
from switchpokepilot.core.logger.logger import Logger


@dataclass
class CommandInitParams:
    controller: Controller
    logger: Logger
    camera: Camera
    image_processor: ImageProcessor


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
        self.image_processor = params.image_processor

    def preprocess(self):
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

    def wait_cancelable(self, duration: float, check_interval: float):
        if check_interval <= 0:
            self.wait(duration)
            return

        elapsed_time = 0
        while self.should_keep_running and elapsed_time < duration:
            remaining_time = duration - elapsed_time
            self.wait(min(remaining_time, check_interval))
            elapsed_time += check_interval

    @staticmethod
    def wait(wait: float):
        if float(wait) > 0.1:
            sleep(wait)
        else:
            current_time = perf_counter()
            while perf_counter() < current_time + wait:
                pass
