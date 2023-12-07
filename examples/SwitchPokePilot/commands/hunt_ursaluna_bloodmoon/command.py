# このコマンドは以下の実装を参考に作成しました。
# https://github.com/Syumiru/Poke-Controller-Modified-PGM/blob/0dd26257521ebfe0f4fcc5fc2b8bc018e269beac/Commands/PythonCommands/ImageProcessingOnly/SV_A0_A0S0GACHIGUMA.py

from switch_pilot_core.command import BaseCommand, CommandAPI, check_should_keep_running
from switch_pilot_core.controller import Button, StickDisplacementPreset


class Command(BaseCommand):
    def __init__(self, api: CommandAPI):
        super().__init__(api)
        self.cfg = None

        self.templates = {}
        self.capture_regions = {}
        self.thresholds = {}

    def process(self):
        try:
            self.cfg = self.config.read()

            self.load_templates()
            self.get_recognition()

            # main loop
            while self.should_keep_running:
                self.attempt()
                self.log_info()

                # Mash A
                self.send_repeat_a_until_battle_start()

                # Battle
                self.wait_for_command_appear()
                self.send_attack_command()

                # Check Speed
                if self.detect_preemptive_attack():
                    self.restart_sv()
                    continue

                if not self.wait_for_battle_finish():
                    self.restart_sv()
                    continue

                # Catch
                self.catch()
                self.skip_pokedex()

                # Check status
                self.goto_status_screen()
                if self.check_status():
                    self.logger.info("目的の個体を捕獲しました。")
                    self.log_info()
                    return
                self.restart_sv()

        except Exception as e:
            self.logger.error(f"{e}")

        finally:
            self.log_info()
            self.logger.info("終了します。")
            self.timer.stop()
            self.postprocess()

    @check_should_keep_running
    def load_templates(self):
        for name in self.cfg["templates"]:
            config = self.cfg["templates"][name]
            self.templates[name] = self.image.read_template(name=config["path"])

            x = config["captureRegion"]["x"]
            y = config["captureRegion"]["y"]
            self.capture_regions[name] = self.image.create_region(x=(x[0], x[1]), y=(y[0], y[1]))

            self.thresholds[name] = config["threshold"]

    @check_should_keep_running
    def send_repeat_a_until_battle_start(self):
        template_name = "battleStarted"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        while self.should_keep_running and not self.capture(template_name).contains(template, threshold):
            self.send_a(duration=0.05)
            self.wait(0.05)

    @check_should_keep_running
    def wait_for_command_appear(self):
        template_name = "battleCommandAppeared"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        while self.should_keep_running and not self.capture(template_name).contains(template, threshold):
            self.wait(0.5)
        self.wait(1)

    @check_should_keep_running
    def send_attack_command(self):
        self.controller.send_repeat(buttons=[Button.A],
                                    times=2,
                                    duration=0.05,
                                    interval=1.0)
        self.wait(1.7)

    @check_should_keep_running
    def detect_preemptive_attack(self):
        template_name = "ursalunaPreemptiveAttacked"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        return self.capture(template_name).contains(template, threshold)

    @check_should_keep_running
    def wait_for_battle_finish(self) -> bool:
        template_name = "catch"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]

        wait_count = 0
        while self.should_keep_running and not self.capture(template_name).contains(template, threshold):
            self.wait(1.0)
            wait_count += 1
            if wait_count >= 60:
                # 60秒待っても終わらない場合は終了
                return False
        return True

    @check_should_keep_running
    def catch(self):
        self.send_a(duration=0.05)
        self.wait(0.6)

        # Select and throw ball
        ball_index = self.cfg["catch"]["ballIndex"]
        if self.cfg["catch"]["ballIndexSeekDirection"] == "right":
            seek_direction = StickDisplacementPreset.RIGHT
        else:
            seek_direction = StickDisplacementPreset.LEFT
        self.controller.send_repeat(l_displacement=seek_direction,
                                    times=ball_index,
                                    duration=0.05,
                                    interval=0.3,
                                    skip_last_interval=False)
        self.send_a(duration=0.05)

        # 演出待機
        self.wait(20)

    @check_should_keep_running
    def skip_pokedex(self):
        if not self.cfg["catch"]["pokedexRegistered"]:
            self.send_a(duration=0.05)
            self.wait(1.05)

    @check_should_keep_running
    def goto_status_screen(self):
        self.send_down()
        self.send_a()
        self.wait(1.0)
        self.send_right()
        self.wait(0.5)
        if self.cfg["checkStatus"]["shouldSaveScreencapture"]:
            self.screenshot()

    @check_should_keep_running
    def check_status(self):
        return self.check_attack() and self.check_speed()

    @check_should_keep_running
    def check_attack(self):
        template_name = "103"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        contains_103 = self.capture(template_name).contains(template, threshold)
        self.logger.info(f"攻撃(103): {contains_103}")
        return contains_103

    @check_should_keep_running
    def check_speed(self):
        if not self.cfg["checkStatus"]["shouldCheckSpeed"]:
            return True

        template_name = "77"
        capture = self.capture(template_name)
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        contains_77 = capture.contains(template, threshold)
        self.logger.info(f"素早さ(77): {contains_77}")

        if self.cfg["checkStatus"]["speedIndividualValue"] == 0:
            return contains_77

        template_name = "78"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        contains_78 = capture.contains(template, threshold)
        self.logger.info(f"素早さ(78): {contains_78}")

        return contains_77 or contains_78

    @check_should_keep_running
    def capture(self, name: str):
        capture_region = self.capture_regions[name]
        return self.video.get_current_frame(region=capture_region).to_gray_scale()

    @check_should_keep_running
    def log_info(self):
        elapsed_time = self.elapsed_time
        self.logger.info(f"経過時間: {elapsed_time.hours}時間{elapsed_time.minutes}分{elapsed_time.seconds}秒")
        self.logger.info(f"実行回数: {self.attempt_count}")
