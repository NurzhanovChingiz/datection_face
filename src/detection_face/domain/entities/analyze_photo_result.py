"""AnalyzePhotoResult is a domain entity aggregating all photo analysis outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from detection_face.domain.entities.camera_health_result import CameraHealthResult


@dataclass(frozen=True)
class AnalyzePhotoResult:
    """Aggregated result of analyzing a photo."""

    camera_health: CameraHealthResult
