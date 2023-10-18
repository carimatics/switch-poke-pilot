import threading

from switchpokepilot.commands.command import Command


class CommandRunner:
    def __init__(self, command: Command | None = None):
        self.command: Command | None = command
        self.__thread: threading.Thread | None = None

    @property
    def is_running(self):
        if self.__thread is None:
            return False
        return not self.__thread.is_alive()

    def start(self):
        self.command.preprocess()

        thread_name = f"{CommandRunner.__name__}:${self.command.process.__name__}:${self.command.name}"
        self.__thread = threading.Thread(target=self.command.process,
                                         name=thread_name,
                                         daemon=True)
        self.__thread.start()

    def stop(self):
        self.command.postprocess()
        self.__thread.join()
        self.__thread = None
