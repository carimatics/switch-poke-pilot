import base64
from dataclasses import dataclass

import cv2

from switchpokepilot.core.image.processor import ImageProcessor
from switchpokepilot.core.logger import Logger
from switchpokepilot.core.utils.env import is_packed
from switchpokepilot.core.utils.os import is_windows


@dataclass
class Point:
    x: int
    y: int


class CropRegion:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


class Camera:
    def __init__(self, capture_size: tuple[int, int], logger: Logger):
        self._id: int = 0
        self._name: str = "Default"

        self.current_frame: cv2.typing.MatLike | None = None
        self.camera: cv2.VideoCapture | None = None
        self.capture_size = capture_size

        self._logger = logger
        self._image_processor = ImageProcessor(logger=self._logger)

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

    def is_opened(self):
        return self.camera is not None and self.camera.isOpened()

    def open(self):
        if not is_packed():
            self._logger.debug("Application is not packed. Skipped open camera.")
            return

        if self.is_opened():
            self._logger.debug("Camera is already opened.")
            self.destroy()

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

    def read_frame(self):
        if not self.is_opened():
            return cv2.mat_wrapper.Mat(arr=[])

        _, self.current_frame = self.camera.read()
        return self.current_frame

    def encoded_current_frame_base64(self):
        if not self.is_opened() or self.current_frame is None:
            return ""

        _, encoded = cv2.imencode(".png", self.current_frame)
        return base64.b64encode(encoded).decode("ascii")

    def get_cropped_current_frame(self,
                                  crop: str | int | None = None,
                                  region: CropRegion | None = None):
        current_frame = self.current_frame
        if current_frame is None:
            return None

        if crop is None:
            return current_frame

        if crop == 1 or crop == "1":
            return current_frame[
                   region.start.y:region.end.y,
                   region.start.x:region.start.y
                   ]

        if crop == 2 or crop == "2":
            return current_frame[
                   region.start.y:region.start.y + region.end.y,
                   region.start.x:region.start.x + region.end.x,
                   ]

        return self.current_frame

    def save_capture(self,
                     file_name: str | None = None,
                     crop: str | int | None = None,
                     crop_region: CropRegion | None = None):
        image = self.get_cropped_current_frame(crop=crop, region=crop_region)
        if image is None:
            self._logger.info(f"Capture skipped: image is None")
            return

        try:
            self._image_processor.save_image(image=image, file_name=file_name)
        except Exception as e:
            self._logger.error(f"Capture failed: {e}")

    def destroy(self):
        if self.is_opened():
            self.camera.release()
            self.camera = None
            self._logger.debug("Camera destroyed.")
