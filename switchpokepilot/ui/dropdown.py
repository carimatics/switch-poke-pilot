from typing import Callable, Self

import flet as ft


class Dropdown(ft.UserControl):
    def __init__(self,
                 label: str,
                 value: str,
                 on_change: Callable[[Self, ft.ControlEvent, int], None],
                 options: [str]):
        super().__init__()
        self.dropdown: ft.Dropdown | None = None

        self.label = label
        self.value = value
        self.on_change = on_change
        self.options = options

    def build(self):
        self.dropdown = ft.Dropdown(
            label=self.label,
            value=self.value,
            on_change=lambda e: self.on_change(self,
                                               e,
                                               self.options.index(e.data)),
            options=[ft.dropdown.Option(o) for o in self.options],
        )
        return self.dropdown
