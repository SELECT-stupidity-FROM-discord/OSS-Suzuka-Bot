from typing import NamedTuple


class Version(NamedTuple):
    major: int
    sub_major: int
    minor: int
    patch: str

    def __str__(self):
        return f"{self.major}.{self.sub_major}.{self.minor} | {self.patch}"

    def full_representation(self):
        return f"v{self.major}.{self.sub_major}.{self.minor}"

del NamedTuple