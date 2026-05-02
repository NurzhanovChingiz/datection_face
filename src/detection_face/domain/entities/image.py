"""Image entity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Image:
    """Image entity."""

    path: str
    image_status: bool
