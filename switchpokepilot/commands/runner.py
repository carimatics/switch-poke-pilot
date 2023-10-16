from switchpokepilot.commands.command import Command


class CommandRunner:
    def __init__(self, command: Command | None = None):
        self.command: Command | None = command

    def start(self):
        try:
            self.command.preprocess()
            self.command.process()
        finally:
            self.command.postprocess()

    def stop(self):
        self.command.postprocess()
