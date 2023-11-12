from switchpokepilot.core.timer import Timer


class CommandTimerAPI:
    def __init__(self, timer: Timer):
        self._timer = timer

    def start(self):
        self._timer.start()

    def stop(self):
        self._timer.stop()

    @property
    def elapsed_time(self):
        return self._timer.elapsed_time
