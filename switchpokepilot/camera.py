import base64
import datetime
import os.path

import cv2

from switchpokepilot.utils.env import is_packed
from switchpokepilot.utils.logger import get_app_logger
from switchpokepilot.utils.os import is_windows

CAPTURE_DIR = "./Captures/"


def write_image(filename, img, params=None) -> bool:
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
        return result
    except Exception as e:
        print(e)
        get_app_logger(__name__).error(f"Image write error: {e}")
        return False


def _get_save_filepath(filename: str, dirname: str | None = None) -> str:
    if dirname is None:
        dirname = CAPTURE_DIR

    if os.path.isabs(filename):
        return filename
    else:
        return os.path.join(dirname, filename)


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class CropAx:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end


class Camera:
    def __init__(self):
        self.current_frame: cv2.typing.MatLike | None = None
        self.camera: cv2.VideoCapture | None = None
        self.capture_size = (1280, 720)

        self.__logger = get_app_logger(__name__)

    def is_opened(self):
        return self.camera is not None and self.camera.isOpened()

    def open(self, camera_id: str | int):
        if not is_packed():
            self.__logger.debug("Application is not packed. Skipped open camera.")
            return

        if self.is_opened():
            self.__logger.debug("Camera is already opened.")
            self.destroy()

        if is_windows():
            self.camera = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
        else:
            self.camera = cv2.VideoCapture(camera_id)

        if not self.is_opened():
            print(f"Camera {camera_id} can't open.")
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

    def save_capture(self,
                     filename: str | None = None,
                     crop: str | int | None = None,
                     crop_ax: CropAx | None = None,
                     img=None):
        if crop_ax is None:
            crop_ax = CropAx(start=Point(0, 0), end=Point(1280, 720))

        if filename is None or filename == "":
            now = datetime.datetime.now()
            filename = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        elif not filename.endswith(".png"):
            filename = f"{filename}.png"

        if crop is None:
            image = self.current_frame
        elif crop == 1 or crop == "1":
            image = self.current_frame[
                    crop_ax.start.y:crop_ax.end.y,
                    crop_ax.start.x:crop_ax.end.x,
                    ]
        elif crop == 2 or crop == "2":
            image = self.current_frame[
                    crop_ax.start.y:crop_ax.start.y + crop_ax.end.y,
                    crop_ax.start.x:crop_ax.start.x + crop_ax.end.x,
                    ]
        elif img is not None:
            image = img
        else:
            image = self.current_frame

        save_path = _get_save_filepath(filename)

        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir) or not os.path.isdir(save_dir):
            os.makedirs(save_dir)
            self.__logger.debug("Capture directory created.")

        try:
            write_image(save_path, image)
            self.__logger.debug(f"Capture succeeded: {save_path}")
        except cv2.error as e:
            self.__logger.error(f"Capture failed: {e}")

    def destroy(self):
        if self.is_opened():
            self.camera.release()
            self.camera = None
            self.__logger.debug("Camera destroyed.")
