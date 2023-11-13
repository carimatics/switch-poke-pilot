class Command:
    def __init__(self, api):
        self.api = api
        self.button = self.api.controller.button
        self.stick = self.api.controller.stick

        self.should_keep_running = False
        self.is_alive = False

        self.templates = {}
        self.capture_regions = {}
        self.thresholds = {}

    @property
    def should_exit(self):
        return not self.should_keep_running

    def process(self):
        try:
            self.api.timer.start()
            self.api.extensions.prepare(self)
            self.config = self.api.config.read()

            self.load_templates()

            self.api.extensions.get_recognition(buttons=[self.button.ZL])

            # main loop
            while self.should_keep_running:
                self.api.extensions.attempt()
                self.log_info()
                if self.should_exit:
                    return

                # Mash A
                self.send_repeat_a_until_battle_start()
                if self.should_exit:
                    return

                # Battle
                self.wait_for_command_appear()
                if self.should_exit:
                    return
                self.send_attack_command()
                if self.should_exit:
                    return

                # Check Speed
                if self.detect_preemptive_attack():
                    self.api.extensions.restart_sv()
                    if self.should_exit:
                        return
                    continue
                else:
                    if not self.wait_for_battle_finish():
                        self.api.extensions.restart_sv()
                        continue
                    if self.should_exit:
                        return

                # Catch
                self.catch()
                if self.should_exit:
                    return
                self.skip_pokedex()
                if self.should_exit:
                    return

                # Check status
                self.goto_status_screen()
                if self.should_exit:
                    return
                if self.check_status():
                    self.api.logger.info("目的の個体を捕獲しました。")
                    self.log_info()
                    return
                self.api.extensions.restart_sv()
        except Exception as e:
            self.api.logger.error(f"{e}")
        finally:
            self.api.logger.info("終了します。")
            self.api.timer.stop()
            self.postprocess()

    def load_templates(self):
        for name in self.config["templates"]:
            config = self.config["templates"][name]
            self.templates[name] = self.api.image.read_template(name=config["path"])

            x = config["captureRegion"]["x"]
            y = config["captureRegion"]["y"]
            self.capture_regions[name] = self.api.image.create_region(x=(x[0], x[1]), y=(y[0], y[1]))

            self.thresholds[name] = config["threshold"]

    def send_repeat_a_until_battle_start(self):
        template_name = "battleStarted"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        while self.should_keep_running and not self.capture(template_name).contains(template, threshold):
            self.api.controller.send_one_shot(buttons=[self.button.A], duration=0.05)
            self.wait(0.05)

    def wait_for_command_appear(self):
        template_name = "battleCommandAppeared"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        while self.should_keep_running and not self.capture(template_name).contains(template, threshold):
            self.wait(0.5)
        self.wait(1)

    def send_attack_command(self):
        self.api.controller.send_repeat(buttons=[self.button.A],
                                        times=2,
                                        duration=0.05,
                                        interval=1.0)
        self.wait(1.7)

    def detect_preemptive_attack(self):
        template_name = "ursalunaPreemptiveAttacked"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        return self.capture(template_name).contains(template, threshold)

    def wait_for_battle_finish(self) -> bool:
        template_name = "catch"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]

        wait_count = 0
        while not self.capture(template_name).contains(template, threshold):
            self.wait(1.0)
            wait_count += 1
            if wait_count >= 60:
                # 60秒待っても終わらない場合は終了
                return False
        return True

    def catch(self):
        self.api.controller.send_one_shot(buttons=[self.button.A],
                                          duration=0.05)
        self.wait(0.6)

        # Select ball
        ball_index = self.config["catch"]["ballIndex"]
        if self.config["catch"]["ballIndexSeekDirection"] == "right":
            seek_direction = self.stick.RIGHT
        else:
            seek_direction = self.stick.LEFT
        self.api.controller.send_repeat(l_stick=seek_direction,
                                        times=ball_index,
                                        duration=0.05,
                                        interval=0.3,
                                        skip_last_interval=False)
        self.api.controller.send_one_shot(buttons=[self.button.A], duration=0.05)

        self.wait(20)

    def skip_pokedex(self):
        if not self.config["catch"]["pokedexRegistered"]:
            self.api.controller.send_one_shot(buttons=[self.button.A], duration=0.05)
            self.wait(1.05)

    def goto_status_screen(self):
        self.api.controller.send_one_shot(l_stick=self.stick.BOTTOM)
        self.api.controller.send_one_shot(buttons=[self.button.A])
        self.wait(1.0)
        self.api.controller.send_one_shot(l_stick=self.stick.RIGHT)
        self.wait(0.5)
        if self.config["checkStatus"]["shouldSaveScreencapture"]:
            self.api.video.capture()

    def check_status(self):
        return self.check_attack() and self.check_speed()

    def check_attack(self):
        template_name = "103"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        achieved = self.capture(template_name).contains(template, threshold)
        self.api.logger.info(f"攻撃(103): {achieved}")
        return achieved

    def check_speed(self):
        if not self.config["checkStatus"]["shouldCheckSpeed"]:
            return True

        template_name = "77"
        capture = self.capture(template_name)
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        contains_77 = capture.contains(template, threshold)
        self.api.logger.info(f"素早さ(77): {contains_77}")

        if self.config["checkStatus"]["speedIndividualValue"] == 0:
            return contains_77

        template_name = "78"
        template = self.templates[template_name]
        threshold = self.thresholds[template_name]
        contains_78 = capture.contains(template, threshold)
        self.api.logger.info(f"素早さ(78): {contains_78}")

        return contains_77 or contains_78

    def capture(self, name: str):
        return self.api.video.get_current_frame().roi(region=self.capture_regions[name]).to_gray_scale()

    def log_info(self):
        elapsed_time = self.api.timer.elapsed_time
        self.api.logger.info(f"経過時間: {elapsed_time.hours}時間{elapsed_time.minutes}分{elapsed_time.seconds}秒")
        self.api.logger.info(f"実行回数: {self.api.extensions.attempt_count}")

    def wait(self, duration: float):
        self.api.extensions.wait(duration)

    def preprocess(self):
        self.should_keep_running = True
        self.is_alive = True

    def postprocess(self):
        self.should_keep_running = False
        self.is_alive = False

    def stop(self):
        self.should_keep_running = False
