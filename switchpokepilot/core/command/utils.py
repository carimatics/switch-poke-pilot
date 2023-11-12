from enum import Enum, auto

from switchpokepilot import reload_config
from switchpokepilot.core.command.base import Command
from switchpokepilot.core.controller.button import Button
from switchpokepilot.core.controller.stick import StickDisplacementPreset as Displacement
from switchpokepilot.core.image.image import Image
from switchpokepilot.core.image.region import ImageRegion
from switchpokepilot.core.timer import Timer


class CropRegionPreset(Enum):
    STATUS_H = auto()
    STATUS_A = auto()
    STATUS_B = auto()
    STATUS_C = auto()
    STATUS_D = auto()
    STATUS_S = auto()


class CropRegionUtils:
    COEFFICIENTS = {
        CropRegionPreset.STATUS_H: {
            "x": {
                "start": 0.71,
                "end": 0.81,
            },
            "y": {
                "start": 0.17,
                "end": 0.275,
            },
        },
        CropRegionPreset.STATUS_A: {
            "x": {
                "start": 0.832,
                "end": 0.915,
            },
            "y": {
                "start": 0.3,
                "end": 0.38,
            },
        },
        CropRegionPreset.STATUS_B: {
            "x": {
                "start": 0.832,
                "end": 0.915,
            },
            "y": {
                "start": 0.48,
                "end": 0.56,
            },
        },
        CropRegionPreset.STATUS_C: {
            "x": {
                "start": 0.61,
                "end": 0.69,
            },
            "y": {
                "start": 0.3,
                "end": 0.38,
            },
        },
        CropRegionPreset.STATUS_D: {
            "x": {
                "start": 0.61,
                "end": 0.69,
            },
            "y": {
                "start": 0.48,
                "end": 0.56,
            },
        },
        CropRegionPreset.STATUS_S: {
            "x": {
                "start": 0.72,
                "end": 0.8,
            },
            "y": {
                "start": 0.56,
                "end": 0.66,
            },
        },
    }

    @staticmethod
    def calc_region(key: CropRegionPreset) -> ImageRegion:
        coefficients = CropRegionUtils.COEFFICIENTS[key]
        return ImageRegion(
            x=(coefficients["x"]["start"], coefficients["x"]["end"]),
            y=(coefficients["y"]["start"], coefficients["y"]["end"])
        )


class CommandUtils:
    def __init__(self, command: Command):
        self.command = command
        self.attempts = 0
        self.timer = Timer()

    @property
    def controller(self):
        return self.command.controller

    @property
    def camera(self):
        return self.command.camera

    @property
    def should_exit(self):
        return not self.command.should_keep_running

    @property
    def elapsed_time(self):
        return self.timer.elapsed_time

    @staticmethod
    def reload_config():
        reload_config()

    def increment_attempts(self):
        self.attempts += 1

    def start_timer(self):
        self.timer.start()

    def stop_timer(self):
        self.timer.stop()

    def get_recognition(self, buttons: list[Button]):
        self.controller.send_repeat(buttons=buttons,
                                    times=3,
                                    duration=0.05,
                                    interval=0.8,
                                    skip_last_interval=False)

    def goto_home(self):
        self.controller.send_one_shot(buttons=[Button.HOME])
        self.command.wait(1)

    def restart_sv(self) -> bool:
        self.goto_home()

        while True:
            # Shutdown Soft
            self.controller.send_one_shot(buttons=[Button.X],
                                          duration=0.05)
            self.command.wait(0.5)
            self.controller.send_one_shot(buttons=[Button.A],
                                          duration=0.05)
            self.command.wait(3.0)

            # Restart
            self.controller.send_repeat(buttons=[Button.A],
                                        times=5,
                                        duration=0.05,
                                        interval=0.5)

            while not self.detect_game_freak_logo():
                self.command.wait(0.1)

            # 検出したら7秒待機してAボタン
            self.command.wait(7)
            self.controller.send_repeat(buttons=[Button.A],
                                        times=5,
                                        duration=0.05,
                                        interval=0.5)

            # フィールドで動けるようになるまで待機
            self.command.wait(18)

            if self.detect_error():
                self.controller.send_one_shot(buttons=[Button.A],
                                              duration=0.05)
                self.command.wait(3.0)
            else:
                return not self.detect_error_required_switch_reboot()

    def detect_game_freak_logo(self):
        height, width, _ = self.camera.current_frame.shape
        capture_region = ImageRegion(x=(0.18, 0.23), y=(0.44, 0.58))
        current_frame = self.camera.get_current_frame(region=capture_region)
        template = Image.from_file("game_freak_logo.png")
        return current_frame.contains(other=template, threshold=0.8)

    def detect_error(self) -> bool:
        current_frame = self.camera.get_current_frame()
        template = Image.from_file("error.png")
        return current_frame.contains(other=template, threshold=0.8)

    def detect_error_required_switch_reboot(self) -> bool:
        current_frame = self.camera.get_current_frame()
        template = Image.from_file("error_required_switch_reboot.png")
        return current_frame.contains(other=template, threshold=0.8)

    def time_leap(self,
                  years: int = 0,
                  months: int = 0,
                  days: int = 0,
                  hours: int = 0,
                  minutes: int = 0,
                  toggle_auto=False,
                  with_reset=False):
        self.goto_home()

        if self.should_exit:
            return

        # Goto System Settings
        self.controller.send_one_shot(l_displacement=Displacement.BOTTOM)
        self.controller.send_repeat(l_displacement=Displacement.RIGHT,
                                    times=5)
        self.controller.send_one_shot(buttons=[Button.A])
        self.command.wait(1.5)

        if self.should_exit:
            return

        # Goto System
        self.controller.send_one_shot(l_displacement=Displacement.BOTTOM,
                                      duration=2)
        self.command.wait(0.3)
        self.controller.send_one_shot(buttons=[Button.A])
        self.command.wait(0.2)

        if self.should_exit:
            return

        # Goto Date and Time
        self.controller.send_one_shot(l_displacement=Displacement.BOTTOM,
                                      duration=0.7)
        self.command.wait(0.2)
        self.controller.send_one_shot(buttons=[Button.A])
        self.command.wait(0.2)

        if self.should_exit:
            return

        if with_reset:
            self.controller.send_one_shot(buttons=[Button.A])
            self.command.wait(0.2)
            self.controller.send_one_shot(buttons=[Button.A])
            self.command.wait(0.2)

        if self.should_exit:
            return

        # Toggle auto clock
        if toggle_auto:
            self.controller.send_one_shot(buttons=[Button.A])
            self.command.wait(0.2)

        if self.should_exit:
            return

        # Goto Current Date and Time
        self.controller.send_repeat(l_displacement=Displacement.BOTTOM,
                                    times=2)
        self.controller.send_one_shot(buttons=[Button.A])
        self.command.wait(0.2)

        if self.should_exit:
            return

        def change(diff: int):
            if diff < 0:
                self.controller.send_repeat(l_displacement=Displacement.BOTTOM,
                                            times=-diff)
            else:
                self.controller.send_repeat(l_displacement=Displacement.TOP,
                                            times=diff)
            self.controller.send_one_shot(l_displacement=Displacement.RIGHT)

        # Change datetime
        change(years)
        change(months)
        change(days)
        change(hours)
        change(minutes)

        # Confirm datetime changes
        self.controller.send_one_shot(buttons=[Button.A])
