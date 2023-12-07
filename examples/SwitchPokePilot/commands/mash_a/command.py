from switch_pilot_core.command import BaseCommand, CommandCancellationError


class Command(BaseCommand):
    def process(self):
        try:
            # main loop
            while self.should_keep_running:
                self.send_a()
                self.wait(0.1)

        except CommandCancellationError:
            self.logger.info("コマンドがキャンセルされました。")
            elapsed_time = self.elapsed_time
            self.logger.info(f"経過時間 {elapsed_time.hours}時間{elapsed_time.minutes}分{elapsed_time.seconds}秒")
