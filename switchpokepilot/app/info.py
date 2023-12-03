from dataclasses import dataclass

_NAME = "Switch Poke Pilot"
_VERSION = {
    "major": 0,
    "minor": 3,
    "patch": 1,
}


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"


@dataclass
class AppInfo:
    name: str
    version: Version


def get_app_info() -> AppInfo:
    return AppInfo(name=_NAME,
                   version=Version(major=_VERSION["major"],
                                   minor=_VERSION["minor"],
                                   patch=_VERSION["patch"]))
