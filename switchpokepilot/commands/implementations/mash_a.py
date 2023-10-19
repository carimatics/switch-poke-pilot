from switchpokepilot.commands.command import Command
from switchpokepilot.controller.controller import Button, Controller
from switchpokepilot.logger import Logger


class MashA(Command):
    def __init__(self, controller: Controller, logger: Logger):
        super().__init__(name="A連打")
        self._controller = controller
        self._logger = logger

    def process(self):
        while self.should_running:
            self._controller.send_one_shot(buttons=[Button.A])
            self._controller.wait(0.5)
            self._logger.debug(f"{self.name}: running...")
        self._logger.debug(f"{self.name}: stopping...")
