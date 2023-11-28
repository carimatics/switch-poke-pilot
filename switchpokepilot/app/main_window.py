import flet as ft


class MainWindow:
    def __init__(self):
        pass

    async def main(self, page: ft.Page):
        await page.add_async(ft.Text("Hello, window!"))
