import math
import os
from typing import Optional

import cv2

from switchpokepilot.core.image.region import ImageRegion


class Image:
    def __init__(self, mat: Optional[cv2.typing.MatLike] = None):
        self._mat: Optional[cv2.typing.MatLike] = mat

    @property
    def width(self) -> int:
        return self._mat.shape[1]

    @property
    def height(self) -> int:
        return self._mat.shape[0]

    @staticmethod
    def from_file(file_name: str, use_gray_scale: bool) -> 'Image':
        if use_gray_scale:
            flags = cv2.IMREAD_GRAYSCALE
        else:
            flags = cv2.IMREAD_COLOR
        return Image(cv2.imread(filename=file_name, flags=flags))

    def save(self, file_name: str) -> bool:
        ext = os.path.splitext(file_name)[1]
        result, n = cv2.imencode(ext, self._mat)

        if result:
            with open(file_name, mode="w+b") as f:
                n.tofile(f)
        return result

    def crop(self, region: ImageRegion) -> 'Image':
        height, width, _ = self._mat.shape
        x0, x1 = math.ceil(width * region.x[0]), math.ceil(width * region.x[1])
        y0, y1 = math.ceil(height * region.y[0]), math.ceil(height * region.y[1])
        return Image(self._mat[y0:y1, x0:x1])

    def to_gray_scale(self) -> 'Image':
        return Image(cv2.cvtColor(self._mat, cv2.COLOR_BGR2GRAY))

    def contains(self, other: 'Image', threshold: float) -> (bool, float):
        result = cv2.matchTemplate(self._mat, other._mat, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold, max_val

    def is_contained_in(self, other: 'Image', threshold: float) -> (bool, float):
        return other.contains(self, threshold)
