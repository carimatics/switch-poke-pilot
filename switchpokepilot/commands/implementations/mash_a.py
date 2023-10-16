from switchpokepilot.commands.command import Command
from switchpokepilot.controller.controller import Button


class MashA(Command):
    NAME = "A連打"

    def process(self):
        while self.is_running:
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.5)
