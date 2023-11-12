from switchpokepilot.core.logger.logger import Logger


class CommandLoggerAPI:
    def __init__(self, logger: Logger):
        self._logger = logger

    def info(self, message: str):
        self._logger.info(message=message)

    def debug(self, message: str):
        self._logger.debug(message=message)

    def warn(self, message: str):
        self._logger.warn(message=message)

    def error(self, message: str):
        self._logger.error(message=message)
