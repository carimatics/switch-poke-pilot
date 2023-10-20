from typing import Callable, Self

import flet as ft


class Button(ft.ElevatedButton):
    def __init__(self,
                 text: str,
                 on_click: Callable[[Self, ft.ControlEvent], None] | None = None,
                 visible: bool = True,
                 disabled: bool = False):
        super().__init__(
            text=text,
            on_click=lambda e: on_click(self, e),
            style=ft.ButtonStyle(
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(2)
                },
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=10),
                }
            ),
            visible=visible,
            disabled=disabled,
        )
