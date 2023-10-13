from switchpokepilot.camera import Camera
from switchpokepilot.utils.logger import get_app_logger


class SwitchPokePilotApp:
    def __init__(self):
        self.__logger = get_app_logger(__name__)
        self.fps = 45
        self.camera = Camera(self.fps)
