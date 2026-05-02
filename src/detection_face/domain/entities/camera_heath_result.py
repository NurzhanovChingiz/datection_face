"""Camera health result entity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraHealthResult:
    """Camera health result entity."""

    camera_id: str
    camera_name: str
    camera_status: str
