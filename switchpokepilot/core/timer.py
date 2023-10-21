import time
from typing import Optional


class Timer:
    def __init__(self):
        self._start_time: float = -1
        self._stop_time: float = -1

    def start(self):
        self._start_time = self._get_current_time()

    def stop(self):
        self._stop_time = self._get_current_time()

    def calculate_elapsed_time(self) -> Optional[(int, int, int)]:
        start_time = self._start_time
        stop_time = self._stop_time

        if start_time <= 0:
            return None

        if start_time > stop_time:
            end_time = self._get_current_time()
        else:
            end_time = stop_time

        elapsed_time_in_seconds = end_time - start_time

        hours = elapsed_time_in_seconds / (60 * 60)
        minutes = (elapsed_time_in_seconds / 60) % 60
        seconds = elapsed_time_in_seconds % 60

        return hours, minutes, seconds

    @staticmethod
    def _get_current_time():
        return time.time()
