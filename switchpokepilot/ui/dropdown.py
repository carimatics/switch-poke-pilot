from typing import Callable, Self

import flet as ft


class Dropdown(ft.UserControl):
    def __init__(self,
                 label: str,
                 value: str,
                 on_change: Callable[[Self, ft.ControlEvent, int], None],
                 options: [str],
                 width: int):
        super().__init__()
        self.dropdown: ft.Dropdown | None = None

        self.label = label
        self.value = value
        self.on_change = on_change
        self.options = options
        self.width = width

    @property
    def label(self) -> str:
        return self._get_attr("label")

    @label.setter
    def label(self, new_value, dirty=True):
        self._set_attr("label", new_value, dirty)

    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, new_value, dirty=True):
        self._set_attr("value", new_value, dirty)

    @property
    def on_change(self):
        return self._get_attr("on_change")

    @on_change.setter
    def on_change(self, new_value, dirty=True):
        self._set_attr("on_change", new_value, dirty)

    @property
    def options(self):
        return self._get_attr("options")

    @options.setter
    def options(self, new_value, dirty=True):
        self._set_attr("options", new_value, dirty)

    def build(self):
        self.dropdown = ft.Dropdown(
            label=self.label,
            value=self.value,
            on_change=lambda e: self.on_change(self,
                                               e,
                                               self.options.index(e.data)),
            options=[ft.dropdown.Option(o) for o in self.options],
            width=self.width,
        )
        return self.dropdown
