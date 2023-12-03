import base64
from typing import Optional

import cv2

from switchpokepilot.core.image.image import Image
from switchpokepilot.core.image.region import ImageRegion
from switchpokepilot.core.logger.logger import Logger
from switchpokepilot.core.utils.device import get_camera_devices
from switchpokepilot.core.utils.env import is_packed
from switchpokepilot.core.utils.os import is_windows


class Camera:
    def __init__(self,
                 capture_size: tuple[int, int],
                 logger: Logger):
        self._id: int = 0
        self._name: str = "Default"

        self.current_frame: Optional[cv2.typing.MatLike] = None
        self.camera: Optional[cv2.VideoCapture] = None
        self.capture_size = capture_size

        self._logger = logger

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, new_value: int):
        self._id = new_value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_value: str):
        self._name = new_value

    @staticmethod
    def get_devices():
        return get_camera_devices()

    def is_opened(self):
        return self.camera is not None and self.camera.isOpened()

    def open(self):
        if not is_packed():
            self._logger.debug("Application is not packed. Skipped open camera.")
            return

        if self.is_opened():
            self._logger.debug("Camera is already opened.")
            self.release()

        if is_windows():
            self.camera = cv2.VideoCapture(self.id, cv2.CAP_DSHOW)
        else:
            self.camera = cv2.VideoCapture(self.id)

        if not self.is_opened():
            print(f"Camera {self.id} can't open.")
            return

        self.resize()

    def resize(self):
        if self.is_opened():
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.capture_size[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.capture_size[1])

    def update_frame(self):
        if not self.is_opened():
            return

        _, self.current_frame = self.camera.read()

    def encoded_current_frame_base64(self):
        if not self.is_opened() or self.current_frame is None:
            return ""

        _, encoded = cv2.imencode(".jpg", self.current_frame)
        return base64.b64encode(encoded).decode("ascii")

    def get_current_frame(self,
                          region: Optional[ImageRegion] = None):
        current_frame = self.current_frame
        if current_frame is None:
            self._logger.debug("current_frame is None")
            return None

        if region is not None:
            return Image(current_frame).roi(region=region)
        return Image(current_frame)

    def save_capture(self,
                     file_path: str,
                     region: Optional[ImageRegion] = None):
        image = self.get_current_frame(region=region)
        if image is None:
            self._logger.info(f"Capture skipped: image is None")
            return

        try:
            image.save(file_path=file_path)
        except Exception as e:
            self._logger.error(f"Capture failed: {e}")

    def release(self):
        if self.is_opened():
            self.camera.release()
            self.camera = None
            self._logger.debug("Camera destroyed.")
