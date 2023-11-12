import threading
from typing import Callable


class CommandRunner:
    def __init__(self, command=None):
        self.command = command
        self._thread: threading.Thread | None = None
        self._on_finish: Callable[[], None] | None = None

    @property
    def is_running(self):
        command = self.command
        if command is None:
            return False

        return command.is_alive

    def start(self, on_finish: Callable[[], None] | None = None):
        if self.command is None:
            raise RuntimeError("Command is not set")

        # prepare
        self._on_finish = on_finish
        self.command.preprocess()

        # start command on new thread
        thread_name = f"{CommandRunner.__name__}:${self.command.process.__name__}"
        self._thread = threading.Thread(target=self._process,
                                        name=thread_name,
                                        daemon=True)
        self._thread.start()

    def _process(self):
        command = self.command
        try:
            command.process()
        finally:
            command.stop()

            on_finish = self._on_finish
            if on_finish is not None:
                on_finish()
            self._on_finish = None

            command.postprocess()
            self.command = None

    def stop(self):
        command = self.command
        if command is not None:
            command.stop()

        thread = self._thread
        try:
            if thread is not None and thread.is_alive():
                thread.join()
        finally:
            self._thread = None

        self.command = None
