"""PredictionWriter gateway — writes prediction results to a sink."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult
    from detection_face.domain.entities.image import Image


class PredictionWriter(ABC):
    """Abstract base for prediction writer."""

    @abstractmethod
    def write(self, image: Image, result: AnalyzePhotoResult) -> None:
        """Write a prediction result.

        Args:
            image: Source image.
            result: Aggregated photo analysis result.
        """
