import threading

from switchpokepilot.commands.base import BaseCommand


class CommandRunner:
    def __init__(self, command: BaseCommand | None = None):
        self.command: BaseCommand | None = command
        self._thread: threading.Thread | None = None

    @property
    def is_running(self):
        if self._thread is None:
            return False
        return self._thread.is_alive()

    def start(self):
        self.command.preprocess()

        thread_name = f"{CommandRunner.__name__}:${self.command.process.__name__}:${self.command.name}"
        self._thread = threading.Thread(target=self.command.process,
                                        name=thread_name,
                                        daemon=True)
        self._thread.start()

    def stop(self):
        self.command.postprocess()
        self._thread.join()
        self._thread = None
