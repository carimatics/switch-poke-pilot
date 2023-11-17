from dataclasses import dataclass


@dataclass
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"
