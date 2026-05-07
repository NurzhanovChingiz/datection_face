"""Black image detection adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from detection_face.domain.ports.black_image_checker import BlackImageChecker

if TYPE_CHECKING:
    from detection_face.domain.entities.image import Image


class CVBlackImageChecker(BlackImageChecker):
    """Detects black images by mean pixel intensity threshold."""

    def __init__(self, threshold: float) -> None:
        """Initialize with detection threshold.

        Args:
            threshold: Mean pixel intensity below which a image is black.
        """
        self._threshold = threshold

    def check(self, image: Image) -> bool:
        """Return True if the image is black.

        Args:
            image: The image to check.

        Returns:
            True if mean pixel intensity is below the threshold for the image pixels.
        """
        return bool(np.mean(image.data) < self._threshold)
