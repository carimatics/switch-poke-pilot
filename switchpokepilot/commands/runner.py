from switchpokepilot.commands.command import Command


class CommandRunner:
    def __init__(self, command: Command | None = None):
        self.command: Command | None = command

    @property
    def is_running(self):
        if self.command is None:
            return False
        return not self.command.should_running

    def start(self):
        try:
            self.command.preprocess()
            self.command.process()
        finally:
            self.command.postprocess()

    def stop(self):
        self.command.postprocess()
