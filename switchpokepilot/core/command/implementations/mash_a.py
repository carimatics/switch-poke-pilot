from switchpokepilot.core.command.base import BaseCommand, CommandInitParams
from switchpokepilot.core.controller.controller import Button


class Command(BaseCommand):
    def __init__(self, params: CommandInitParams):
        super().__init__(params=params)
        self.name = "A連打"

    def process(self):
        while self.should_running:
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.5)
            self.logger.debug(f"{self.name}: running...")
        self.logger.debug(f"{self.name}: stopping...")
