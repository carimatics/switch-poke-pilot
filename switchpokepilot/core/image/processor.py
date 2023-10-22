import datetime
import os
import typing

import cv2

from switchpokepilot.core.logger import Logger
from switchpokepilot.core.utils.directories import get_dir, DirectoryKind


def _normalize_file_name(file_name: str | None = None) -> str:
    if file_name is None or file_name == "":
        now = datetime.datetime.now()
        return f"{now.strftime("%Y-%m-%d_%H-%M-%S-%f")}.png"

    if not file_name.endswith(".png"):
        return f"{file_name}.png"


def _get_capture_file_path(file_name: str,
                           dir_name: str | None = None) -> str:
    if os.path.isabs(file_name):
        return file_name

    if dir_name is None:
        dir_name = get_dir(DirectoryKind.CAPTURES)

    return os.path.join(dir_name, file_name)


def _get_template_file_path(file_name: str,
                            dir_name: str | None = None) -> str:
    if os.path.isabs(file_name):
        return file_name

    if dir_name is None:
        dir_name = get_dir(DirectoryKind.TEMPLATES)

    return os.path.join(dir_name, file_name)


def _get_mask_file_path(file_name: str,
                        dir_name: str | None = None) -> str:
    if os.path.isabs(file_name):
        return file_name

    if dir_name is None:
        dir_name = get_dir(DirectoryKind.MASKS)

    return os.path.join(dir_name, file_name)


def _write_image(file_name: str,
                 image: cv2.typing.MatLike,
                 params: typing.Sequence[int] | None = None):
    ext = os.path.splitext(file_name)[1]
    result, n = cv2.imencode(ext, image, params)

    if result:
        with open(file_name, mode="w+b") as f:
            n.tofile(f)
    return result


def _read_image(file_name: str,
                use_gray_scale: bool = True):
    if use_gray_scale:
        flags = cv2.IMREAD_GRAYSCALE
    else:
        flags = cv2.IMREAD_COLOR
    return cv2.imread(filename=file_name, flags=flags)


class ImageProcessor:
    def __init__(self, logger: Logger):
        self._logger = logger

    def match_template(self,
                       image: cv2.typing.MatLike,
                       template_path: str,
                       use_gray_scale: bool = True,
                       mask_path: str | None = None):
        try:
            if use_gray_scale:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            template = _read_image(file_name=_get_template_file_path(template_path),
                                   use_gray_scale=use_gray_scale)
            if mask_path is None:
                mask = None
                method = cv2.TM_CCOEFF_NORMED
            else:
                mask = _read_image(file_name=_get_mask_file_path(mask_path),
                                   use_gray_scale=True)
                method = cv2.TM_CCORR_NORMED

            return cv2.matchTemplate(image, template, method, mask)
        except Exception as e:
            self._logger.error(f"ImageProcessor#match_template: {e}")
            raise e

    def contains_template(self,
                          image: cv2.typing.MatLike,
                          template_path: str,
                          threshold: float = 0.7,
                          use_gray_scale: bool = True,
                          mask_path: str | None = None):
        result = self.match_template(image=image,
                                     template_path=template_path,
                                     use_gray_scale=use_gray_scale,
                                     mask_path=mask_path)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        contains = max_val >= threshold
        if contains:
            self._logger.debug(f"ImageProcessor#contains_template: Template contains.")
        return contains

    def save_image(self,
                   image: cv2.typing.MatLike,
                   file_name: str | None = None):
        file_name = _normalize_file_name(file_name=file_name)
        save_path = _get_capture_file_path(file_name=file_name)
        save_dir = os.path.dirname(save_path)

        if not os.path.exists(save_dir) or not os.path.isdir(save_dir):
            os.makedirs(save_dir, mode=0o755)
            self._logger.info("ImageProcessor#save_image: Capture folder created.")

        try:
            _write_image(save_path, image)
            self._logger.info(f"ImageProcessor#save_image: Save {save_path}")
        except Exception as e:
            self._logger.error(f"ImageProcessor#save_image: Capture failed. {e}")
