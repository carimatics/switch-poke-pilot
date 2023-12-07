import multiprocessing
from queue import Empty, Queue
from typing import Optional

import flet as ft
import pygame.camera
from switch_pilot_core.path import Path

from switchpokepilot.app.mainwindow.main_window import MainWindow


def _open_main_window_app(queue: multiprocessing.Queue):
    pygame.camera.init()

    window = MainWindow(queue=queue)
    path = Path()
    ft.app(
        port=0,
        target=window.main,
        assets_dir=path.user_directory(),
    )


class MainWindowProcess:
    def __init__(self):
        self._queue = multiprocessing.Queue()
        self._process = multiprocessing.Process(target=_open_main_window_app,
                                                args=(self._queue,))

    def is_alive(self):
        return self._process.is_alive()

    def start(self):
        self._process.start()

    def join(self):
        try:
            self._process.join(timeout=0.5)
        finally:
            pass

    def get_object(self,
                   block: bool = True,
                   timeout: Optional[float] = None):
        return self._queue.get(block=block, timeout=timeout)

    def put_object(self,
                   obj: object,
                   block: bool = True,
                   timeout: Optional[float] = None):
        self._queue.put(obj, block=block, timeout=timeout)

    def close_queue(self):
        self._queue.close()


class MainWindowProcessPool:
    def __init__(self):
        self._queue = Queue()
        self._processes: list[MainWindowProcess] = []

    @property
    def count(self):
        return len(self._processes)

    @property
    def qsize(self):
        return self._queue.qsize()

    def start_new_process(self):
        process = MainWindowProcess()
        self._processes.append(process)
        process.start()

    def broadcast_object(self,
                         obj: object,
                         block: bool = True,
                         timeout: Optional[float] = None):
        for process in self._processes:
            if process.is_alive():
                process.put_object(obj, block=block, timeout=timeout)
        self._shake()

    def receive_object(self,
                       block: bool = True,
                       timeout: Optional[float] = None):
        for process in self._processes:
            self._flush_objects(process)
        self._shake()
        return self._queue.get(block=block, timeout=timeout)

    def _shake(self):
        for process in self._processes:
            if not process.is_alive():
                process.join()
                self._flush_objects(process)
                process.close_queue()
                self._processes.remove(process)

    def _flush_objects(self, process: MainWindowProcess):
        while True:
            try:
                obj = process.get_object(block=False)
                self._queue.put(obj)
            except ValueError:
                # when queue closed
                break
            except Empty:
                # when queue empty
                break
