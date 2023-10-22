from switchpokepilot import reload_config
from switchpokepilot.core.command.base import Command
from switchpokepilot.core.controller.controller import (
    Controller,
    Button,
    StickDisplacementPreset as Displacement,
)
from switchpokepilot.core.timer import Timer


class CommandUtils:
    def __init__(self, command: Command, controller: Controller):
        self.command = command
        self.controller = controller

        self.attempts = 0

        self.timer = Timer()
        self.timer.start()

    @property
    def should_exit(self):
        return not self.command.should_keep_running

    @property
    def elapsed_time(self):
        return self.timer.calculate_elapsed_time()

    @staticmethod
    def reload_config():
        reload_config()

    def increment_attempts(self):
        self.attempts += 1

    def get_recognition(self, buttons: list[Button]):
        self.controller.send_repeat(buttons=buttons,
                                    count=3,
                                    duration=0.05,
                                    interval=0.8,
                                    skip_last_interval=False)

    def time_leap(self,
                  years: int = 0,
                  months: int = 0,
                  days: int = 0,
                  hours: int = 0,
                  minutes: int = 0,
                  toggle_auto=False,
                  with_reset=False):
        # Goto Home
        self.controller.send_one_shot(buttons=[Button.HOME])
        self.controller.wait(1)

        if self.should_exit:
            return

        # Goto System Settings
        self.controller.send_one_shot(l_displacement=Displacement.DOWN)
        self.controller.send_repeat(l_displacement=Displacement.RIGHT,
                                    count=5)
        self.controller.send_one_shot(buttons=[Button.A])
        self.controller.wait(1.5)

        if self.should_exit:
            return

        # Goto System
        self.controller.send_one_shot(l_displacement=Displacement.DOWN,
                                      duration=2)
        self.controller.wait(0.3)
        self.controller.send_one_shot(buttons=[Button.A])
        self.controller.wait(0.2)

        if self.should_exit:
            return

        # Goto Date and Time
        self.controller.send_one_shot(l_displacement=Displacement.DOWN,
                                      duration=0.7)
        self.controller.wait(0.2)
        self.controller.send_one_shot(buttons=[Button.A])
        self.controller.wait(0.2)

        if self.should_exit:
            return

        if with_reset:
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.2)
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.2)

        if self.should_exit:
            return

        # Toggle auto clock
        if toggle_auto:
            self.controller.send_one_shot(buttons=[Button.A])
            self.controller.wait(0.2)

        if self.should_exit:
            return

        # Goto Current Date and Time
        self.controller.send_repeat(l_displacement=Displacement.DOWN,
                                    count=2)
        self.controller.send_one_shot(buttons=[Button.A])
        self.controller.wait(0.2)

        if self.should_exit:
            return

        def change(diff: int):
            if diff < 0:
                self.controller.send_repeat(l_displacement=Displacement.DOWN,
                                            count=-diff)
            else:
                self.controller.send_repeat(l_displacement=Displacement.UP,
                                            count=diff)
            self.controller.send_one_shot(l_displacement=Displacement.RIGHT)

        # Change datetime
        change(years)
        change(months)
        change(days)
        change(hours)
        change(minutes)

        # Confirm datetime changes
        self.controller.send_one_shot(buttons=[Button.A])
