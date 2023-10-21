from switchpokepilot.core.command.base import Command
from switchpokepilot.core.controller.controller import Button


class MashA(Command):
    NAME = "A連打"

    def process(self):
        while self.should_keep_running:
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.5)
            self.logger.debug(f"{MashA.NAME}: running...")
        self.logger.debug(f"{MashA.NAME}: stopping...")
        self.finish()
