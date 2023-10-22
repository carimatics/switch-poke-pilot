import datetime
from configparser import ConfigParser
from dataclasses import dataclass
from distutils.util import strtobool

from switchpokepilot import config
from switchpokepilot.core.camera import CropRegion
from switchpokepilot.core.command.base import Command, CommandInitParams
from switchpokepilot.core.command.utils import CommandUtils, CropRegionUtils, CropRegionPreset
from switchpokepilot.core.controller.controller import Button, StickDisplacementPreset as Displacement
from switchpokepilot.core.logger import Logger

CONFIG_BASE_SECTION = "command.hunt_ursaluna_bloodmoon"


class HuntUrsalunaBloodmoon(Command):
    NAME = "ガチグマ(アカツキ)厳選"

    def __init__(self, params: CommandInitParams):
        super().__init__(params=params)
        self.generation = "9"
        self.utils = CommandUtils(command=self)
        self.config: HuntUrsalunaBloodmoonConfig | None = None

    def process(self):
        try:
            # Initialize
            self.utils.start_timer()
            self.utils.reload_config()

            # Parse config
            self.config = HuntUrsalunaBloodmoonConfig(config)
            is_config_valid = self.config.validate(logger=self.logger)
            if not is_config_valid:
                return

            # Main loop
            while self.should_keep_running:
                self.utils.increment_attempts()
                self._log_command_status()

                self._send_repeat_a_until_battle_start()
                self._wait_for_command_appear()
                self._send_attack_command()

                # Check speed
                if self.config.status.should_check_speed and self._detect_ursaluna_preemptive_attack():
                    restart_succeeded = self.utils.restart_sv()
                    if not restart_succeeded:
                        return
                    continue
                else:
                    self._wait_for_battle_finish()

                self._catch_ursaluna()
                self._skip_pokedex()

                # Check status
                self._goto_status_screen()
                achieved = self._check_ursaluna_status()
                if achieved:
                    return

                restart_succeeded = self.utils.restart_sv()
                if not restart_succeeded:
                    return

        finally:
            self.utils.stop_timer()
            self.finish()

    def postprocess(self):
        self.utils = None
        super().postprocess()

    def _send_repeat_a_until_battle_start(self):
        while not self._detect_battle_started():
            self.controller.send_one_shot(buttons=[Button.A],
                                          duration=0.05)
            self.controller.wait(0.05)

    def _wait_for_command_appear(self):
        while not self._detect_battle_command_appeared():
            self.controller.wait(0.5)
        self.controller.wait(1)

    def _send_attack_command(self):
        self.controller.send_repeat(buttons=[Button.A],
                                    count=2,
                                    duration=0.05,
                                    interval=0.8)
        self.controller.wait(1.7)

    def _wait_for_battle_finish(self):
        # ターン経過待機
        self.controller.wait(36.5)
        # 撃破後演出待機
        self.controller.wait(16.5)

    def _detect_battle_started(self) -> bool:
        return self.image_processor.contains_template(image=self.camera.current_frame,
                                                      template_path=self._template_path("voice.png"),
                                                      threshold=self.config.template_matching.battle_started)

    def _detect_battle_command_appeared(self) -> bool:
        return self.image_processor.contains_template(image=self.camera.current_frame,
                                                      template_path=self._template_path("battle_command.png"),
                                                      threshold=self.config.template_matching.command_appeared)

    def _detect_ursaluna_preemptive_attack(self) -> bool:
        capture_region = CropRegion(x=(185, 495),
                                    y=(530, 562))
        image = self.camera.get_cropped_current_frame(region=capture_region)
        # TODO: あとで消す
        self.image_processor.save_image(image)

        threshold = self.config.template_matching.ursaluna_attacked_preemptive
        return self.image_processor.contains_template(image=image,
                                                      template_path="ursaluna_attack.png",
                                                      threshold=threshold)

    def _catch_ursaluna(self):
        # 捕まえるを選択
        self.controller.send_one_shot(buttons=[Button.A],
                                      duration=0.05)
        self.controller.wait(0.6)

        displacement_for_select_ball = Displacement.RIGHT
        if self.config.ball_index_seek_direction == "Left":
            displacement_for_select_ball = Displacement.LEFT

        # ボールを選択して投げる
        self.controller.send_repeat(l_displacement=displacement_for_select_ball,
                                    count=self.config.ball_index,
                                    duration=0.05,
                                    interval=0.3,
                                    skip_last_interval=False)
        self.controller.send_one_shot(buttons=[Button.A],
                                      duration=0.05)
        # 演出待機
        self.controller.wait(20)

    def _skip_pokedex(self):
        if not self.config.pokedex_registered:
            self.controller.send_one_shot(buttons=[Button.A],
                                          duration=0.05)
            self.controller.wait(1.05)

    def _goto_status_screen(self):
        self.controller.send_one_shot(l_displacement=Displacement.DOWN)
        self.controller.send_one_shot(buttons=[Button.A])
        self.controller.wait(1)
        self.controller.send_one_shot(l_displacement=Displacement.RIGHT)

    def _check_ursaluna_status(self) -> bool:
        return (self._check_ursaluna_attack_actual_value() and
                self._check_ursaluna_speed_actual_value() and
                self._check_ursaluna_attack_individual_value())

    def _check_ursaluna_attack_actual_value(self) -> bool:
        height, width, _ = self.camera.current_frame.shape
        capture_region = CropRegionUtils.calc_region(key=CropRegionPreset.STATUS_A,
                                                     height=height,
                                                     width=width)
        image = self.camera.get_cropped_current_frame(region=capture_region)
        threshold = self.config.template_matching.actual_value
        return self.image_processor.contains_template(image=image,
                                                      template_path="103.png",
                                                      threshold=threshold)

    def _check_ursaluna_speed_actual_value(self) -> bool:
        height, width, _ = self.camera.current_frame.shape
        capture_region = CropRegionUtils.calc_region(key=CropRegionPreset.STATUS_S,
                                                     height=height,
                                                     width=width)
        image = self.camera.get_cropped_current_frame(region=capture_region)
        threshold = self.config.template_matching.actual_value
        if self.config.status.speed_individual_value == 0:
            template_path = "77.png"
        else:
            template_path = "78.png"

        return self.image_processor.contains_template(image=image,
                                                      template_path=template_path,
                                                      threshold=threshold)

    def _check_ursaluna_attack_individual_value(self) -> bool:
        # TODO: ちゃんと実装する
        return True

    def _log_command_status(self):
        elapsed = self.utils.elapsed_time
        self.logger.info(f"現在時刻: {datetime.datetime.now()}")
        self.logger.info(f"試行回数: {self.utils.attempts}回目")
        self.logger.info(f"経過時間: {elapsed.hours}時間{elapsed.minutes}分{elapsed.seconds}秒")

    @staticmethod
    def _template_path(file: str):
        return f"hunt_ursaluna_bloodmoon/{file}"


class HuntUrsalunaBloodmoonConfig:
    def __init__(self, parser: ConfigParser):
        base_section = parser[CONFIG_BASE_SECTION]
        self.ball_index_seek_direction = base_section["BallIndexSeekDirection"]
        self.ball_index = int(base_section["BallIndex"])
        self.pokedex_registered = strtobool(base_section["PokedexRegistered"])

        status_section = parser[f"{CONFIG_BASE_SECTION}.status"]
        self.status = StatusConfig(
            should_check_speed=bool(strtobool(status_section["ShouldCheckSpeed"])),
            should_check_status=bool(strtobool(status_section["ShouldCheckStatus"])),
            should_save_screenshot=bool(strtobool(status_section["ShouldSaveScreenshot"])),
            attack_individual_value=int(status_section["AttackIndividualValue"]),
            speed_individual_value=int(status_section["SpeedIndividualValue"]),
        )

        template_matching_section = parser[f"{CONFIG_BASE_SECTION}.template_matching"]
        self.template_matching = TemplateMatchingThresholdConfig(
            battle_started=float(template_matching_section["BattleStarted"]),
            command_appeared=float(template_matching_section["CommandAppeared"]),
            ursaluna_attacked_preemptive=float(template_matching_section["UrsalunaAttackedPreemptive"]),
            actual_value=float(template_matching_section["ActualValue"]),
            individual_value=float(template_matching_section["IndividualValue"]),
        )

    def validate(self, logger: Logger) -> bool:
        if self.ball_index_seek_direction not in ["Right", "Light"]:
            logger.error("Invalid BallIndexSeeKDirection: required Right or Left")
            return False

        if self.ball_index < 0:
            logger.error("Invalid BallIndex: require BallIndex >= 0")
            return False

        if self.status.attack_individual_value not in [0, 1]:
            logger.error("Invalid AttackIndividualValue: 0 or 1")
            return False

        if self.status.speed_individual_value not in [0, 1]:
            logger.error("Invalid SpeedIndividualValue: 0 or 1")
            return False

        return True


@dataclass
class StatusConfig:
    should_check_speed: bool
    should_check_status: bool
    should_save_screenshot: bool
    attack_individual_value: int
    speed_individual_value: int


@dataclass
class TemplateMatchingThresholdConfig:
    battle_started: float
    command_appeared: float
    ursaluna_attacked_preemptive: float
    actual_value: float
    individual_value: float
