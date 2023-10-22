import base64

import cv2

from switchpokepilot.core.image.processor import ImageProcessor
from switchpokepilot.core.logger import Logger
from switchpokepilot.core.utils.env import is_packed
from switchpokepilot.core.utils.os import is_windows


class InvalidRegionError(Exception):
    pass


class CropRegion:
    def __init__(self, x: tuple[int, int], y: tuple[int, int]):
        if x[0] >= x[1] or y[0] >= y[1]:
            raise InvalidRegionError
        self.x = x
        self.y = y


class Camera:
    def __init__(self,
                 capture_size: tuple[int, int],
                 image_processor: ImageProcessor,
                 logger: Logger):
        self._id: int = 0
        self._name: str = "Default"

        self.current_frame: cv2.typing.MatLike | None = None
        self.camera: cv2.VideoCapture | None = None
        self.capture_size = capture_size

        self._logger = logger
        self._image_processor = image_processor

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
                                  region: CropRegion | None = None):
        current_frame = self.current_frame
        if current_frame is None:
            self._logger.debug("current_frame is None")
            return None

        height, width, _ = current_frame.shape
        if region is not None:
            return current_frame[
                   region.y[0]:region.y[1],
                   region.x[0]:region.x[1],
                   ]

        return current_frame

    def save_capture(self,
                     file_name: str | None = None,
                     crop_region: CropRegion | None = None):
        image = self.get_cropped_current_frame(region=crop_region)
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
