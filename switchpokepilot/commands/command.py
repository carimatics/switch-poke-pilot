from abc import ABCMeta, abstractmethod

from switchpokepilot.controller.controller import Controller


class Command(metaclass=ABCMeta):
    def __init__(self, controller: Controller):
        self.is_running = False
        self.controller = controller

    @abstractmethod
    def start(self, postprocess=None):
        raise NotImplementedError

    @abstractmethod
    def end(self):
        raise NotImplementedError
