from time import sleep, perf_counter

from switchpokepilot.core.camera import Camera
from switchpokepilot.core.controller.button import Button
from switchpokepilot.core.controller.controller import Controller
from switchpokepilot.core.controller.stick import StickDisplacementPreset as Displacement
from switchpokepilot.core.image.image import Image
from switchpokepilot.core.image.region import ImageRegion
from switchpokepilot.core.path.path import Path


class CommandExtensionsAPI:
    def __init__(self,
                 controller: Controller,
                 camera: Camera,
                 path: Path):
        self._command = None
        self._controller = controller
        self._camera = camera
        self._path = path
        self._attempt_count = 0

    def prepare(self, command):
        self._command = command

    @property
    def attempt_count(self):
        return self._attempt_count

    @property
    def should_keep_running(self):
        if self._command.should_keep_running is None:
            return False
        return self._command.should_keep_running

    @property
    def should_exit(self):
        return not self.should_keep_running

    def attempt(self):
        self._attempt_count += 1

    def wait(self, duration: float, check_interval: float = 1.0):
        if check_interval <= 0:
            check_interval = 1.0

        if float(duration) > 0.1:
            elapsed = 0
            while self.should_keep_running and elapsed < duration:
                remaining = duration - elapsed
                sleep_duration = min(remaining, check_interval)
                sleep(sleep_duration)
                elapsed += sleep_duration
        else:
            current_time = perf_counter()
            while perf_counter() < current_time + duration:
                pass

    def get_recognition(self, buttons: list[Button]):
        self._controller.send_repeat(buttons=buttons,
                                     times=3,
                                     duration=0.05,
                                     interval=0.8,
                                     skip_last_interval=False)

    def goto_home(self):
        self._controller.send_one_shot(buttons=[Button.HOME])
        self.wait(1)

    def restart_sv(self):
        self.goto_home()
        if self.should_exit:
            return

        # Shutdown Software
        self._controller.send_one_shot(buttons=[Button.X],
                                       duration=0.05)
        if self.should_exit:
            return
        self.wait(0.5)
        if self.should_exit:
            return
        self._controller.send_one_shot(buttons=[Button.A],
                                       duration=0.05)
        if self.should_exit:
            return
        self.wait(3.0)
        if self.should_exit:
            return

        # Launch Software
        self._controller.send_repeat(buttons=[Button.A],
                                     times=5,
                                     duration=0.05,
                                     interval=0.5)
        if self.should_exit:
            return

        # Wait for detect game freak logo
        logo_template = Image.from_file(self._path.template("game_freak_logo.png"))
        capture_region = ImageRegion(x=(0.18, 0.23), y=(0.44, 0.58))
        while not logo_template.is_contained_in(self._camera.get_current_frame(capture_region), threshold=0.8):
            if self.should_exit:
                return
            self.wait(0.1)
        if self.should_exit:
            return

        # Wait for 7 seconds and press A button
        self.wait(7.0)
        if self.should_exit:
            return
        self._controller.send_repeat(buttons=[Button.A],
                                     times=5,
                                     duration=0.05,
                                     interval=0.5)
        if self.should_exit:
            return

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
        self._controller.send_one_shot(l_displacement=Displacement.BOTTOM)
        if self.should_exit:
            return
        self._controller.send_repeat(l_displacement=Displacement.RIGHT,
                                     times=5)
        if self.should_exit:
            return
        self._controller.send_one_shot(buttons=[Button.A])
        if self.should_exit:
            return
        self._command.wait(1.5)

        if self.should_exit:
            return

        # Goto System
        self._controller.send_one_shot(l_displacement=Displacement.BOTTOM,
                                       duration=2)
        if self.should_exit:
            return
        self._command.wait(0.3)
        if self.should_exit:
            return
        self._controller.send_one_shot(buttons=[Button.A])
        if self.should_exit:
            return
        self._command.wait(0.2)

        if self.should_exit:
            return

        # Goto Date and Time
        self._controller.send_one_shot(l_displacement=Displacement.BOTTOM,
                                       duration=0.7)
        if self.should_exit:
            return
        self._command.wait(0.2)
        if self.should_exit:
            return
        self._controller.send_one_shot(buttons=[Button.A])
        if self.should_exit:
            return
        self._command.wait(0.2)
        if self.should_exit:
            return

        if self.should_exit:
            return

        if with_reset:
            self._controller.send_one_shot(buttons=[Button.A])
            if self.should_exit:
                return
            self._command.wait(0.2)
            if self.should_exit:
                return
            self._controller.send_one_shot(buttons=[Button.A])
            if self.should_exit:
                return
            self._command.wait(0.2)

        if self.should_exit:
            return

        # Toggle auto clock
        if toggle_auto:
            self._controller.send_one_shot(buttons=[Button.A])
            if self.should_exit:
                return
            self._command.wait(0.2)

        if self.should_exit:
            return

        # Goto Current Date and Time
        self._controller.send_repeat(l_displacement=Displacement.BOTTOM,
                                     times=2)
        if self.should_exit:
            return
        self._controller.send_one_shot(buttons=[Button.A])
        if self.should_exit:
            return
        self._command.wait(0.2)

        if self.should_exit:
            return

        def change(diff: int):
            if diff < 0:
                self._controller.send_repeat(l_displacement=Displacement.BOTTOM,
                                             times=-diff)
            else:
                self._controller.send_repeat(l_displacement=Displacement.TOP,
                                             times=diff)
            self._controller.send_one_shot(l_displacement=Displacement.RIGHT)

        # Change datetime
        change(years)
        if self.should_exit:
            return
        change(months)
        if self.should_exit:
            return
        change(days)
        if self.should_exit:
            return
        change(hours)
        if self.should_exit:
            return
        change(minutes)
        if self.should_exit:
            return

        # Confirm datetime changes
        self._controller.send_one_shot(buttons=[Button.A])
