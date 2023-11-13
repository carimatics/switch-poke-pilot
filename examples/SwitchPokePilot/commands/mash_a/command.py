class Command:
    def __init__(self, api):
        self.api = api
        self.button = self.api.controller.button

        self.should_keep_running = False
        self.is_alive = False

    def process(self):
        try:
            self.api.timer.start()
            self.api.extensions.prepare(self)

            # main loop
            while self.should_keep_running:
                self.api.controller.send_one_shot(buttons=self.button.A)
                self.api.extensions.wait(0.5)

            elapsed_time = self.api.timer.elapsed_time
            self.api.logger.info(f"経過時間 {elapsed_time.hours}時間{elapsed_time.minutes}分{elapsed_time.seconds}秒")
        finally:
            self.api.timer.stop()
            self.postprocess()

    def preprocess(self):
        self.should_keep_running = True
        self.is_alive = True

    def postprocess(self):
        self.should_keep_running = False
        self.is_alive = False

    def stop(self):
        self.should_keep_running = False
