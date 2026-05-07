"""Port for black image detection."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from detection_face.domain.entities.image import Image


class BlackImageChecker(ABC):
    """Abstract base for black image detection."""

    @abstractmethod
    def check(self, image: Image) -> bool:
        """Return True if the image is black.

        Args:
            image: The image to check.

        Returns:
            True if the image is detected as black.
        """
