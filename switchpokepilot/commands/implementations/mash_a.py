from switchpokepilot.commands.command import Command
from switchpokepilot.controller.controller import Button, Controller
from switchpokepilot.logger import Logger


class MashA(Command):
    def __init__(self, controller: Controller, logger: Logger):
        super().__init__(name="A連打")
        self.__controller = controller
        self.__logger = logger

    def process(self):
        while self.should_running:
            self.__controller.send_one_shot(buttons=[Button.A])
            self.__controller.wait(0.5)
            self.__logger.debug("MashA: is running...")
        self.__logger.debug("MashA: is stopping...")
