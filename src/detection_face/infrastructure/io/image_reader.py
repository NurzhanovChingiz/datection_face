"""OpenCV image reader adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2

from detection_face.application.gateways.image_source import ImageSource
from detection_face.domain.entities.image import Image

if TYPE_CHECKING:
    from pathlib import Path


class CVImageReader(ImageSource):
    """Loads images from disk using OpenCV."""

    def load(self, path: Path) -> Image:
        """Load an image from disk.

        Args:
            path: Path to the image file.

        Returns:
            Image with loaded pixel data.

        Raises:
            FileNotFoundError: If the image cannot be read.
        """
        data = cv2.imread(str(path))
        if data is None:
            raise FileNotFoundError(path)
        return Image(image_id=path.stem, path=path, data=data, shape=data.shape)
