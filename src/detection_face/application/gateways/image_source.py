"""ImageSource gateway — loads images from a source."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from detection_face.domain.entities.image import Image


class ImageSource(ABC):
    """Abstract base for image source."""

    @abstractmethod
    def load(self, path: Path) -> Image:
        """Load an image from the given path.

        Args:
            path: Path to the image file.

        Returns:
            Loaded image.
        """
