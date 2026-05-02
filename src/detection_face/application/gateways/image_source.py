"""Image source gateway."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from detection_face.domain.entities.image import Image


class ImageSource(ABC):
    """Image source gateway."""

    @abstractmethod
    def get_image(self) -> Image:
        """Get the image."""
