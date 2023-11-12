from typing import Optional

from switchpokepilot.core.camera import Camera
from switchpokepilot.core.image.image import Image
from switchpokepilot.core.image.region import ImageRegion
from switchpokepilot.core.path.path import Path


class CommandVideoAPI:
    def __init__(self, camera: Camera, path: Path):
        self._path = path
        self._camera = camera

    def capture(self, region: Optional[ImageRegion] = None):
        file_path = self._path.capture()
        return self._camera.save_capture(region=region, file_path=file_path)

    def get_current_frame(self, region: Optional[ImageRegion] = None, key: Optional[str] = None) -> Optional[Image]:
        if region is None and key is not None:
            region = self.get_region_preset(key=key)
        return self._camera.get_current_frame(region=region)

    @staticmethod
    def get_region_preset(key: str) -> Optional[ImageRegion]:
        return ({
            "STATUS_H": ImageRegion(x=(0.71, 0.81), y=(0.17, 0.275)),
            "STATUS_A": ImageRegion(x=(0.832, 0.915), y=(0.3, 0.38)),
            "STATUS_B": ImageRegion(x=(0.832, 0.915), y=(0.48, 0.56)),
            "STATUS_C": ImageRegion(x=(0.61, 0.69), y=(0.3, 0.38)),
            "STATUS_D": ImageRegion(x=(0.61, 0.69), y=(0.48, 0.56)),
            "STATUS_S": ImageRegion(x=(0.72, 0.8), y=(0.56, 0.66)),
        }).get(key, None)
