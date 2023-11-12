from switchpokepilot.core.config.config import Config


class CommandConfigAPI:
    def __init__(self, config: Config, command: str):
        self._config = config
        self._command = command

    def read(self):
        return self._config.read_command_config(name=self._command)
