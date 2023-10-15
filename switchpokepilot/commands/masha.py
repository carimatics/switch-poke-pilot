from switchpokepilot.commands.command import Command
from switchpokepilot.controller.controller import Button


class MashA(Command):
    NAME = "A連打"

    def start(self, postprocess=None):
        self.is_running = True
        while self.is_running:
            self.controller.one_shot_buttons(buttons=[Button.A])
            self.controller.wait(0.5)

    def end(self):
        self.is_running = False
