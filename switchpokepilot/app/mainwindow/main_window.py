import multiprocessing

import flet as ft


class MainWindow:
    def __init__(self, queue: multiprocessing.Queue):
        self._queue = queue

    async def main(self, page: ft.Page):
        await page.add_async(ft.Text("Hello, window!"))
