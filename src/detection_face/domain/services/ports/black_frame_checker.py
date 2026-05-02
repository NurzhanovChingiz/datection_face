"""Port interface for detecting black frames."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from detection_face.domain.entities.image import Image


class BlackFrameChecker(ABC):
    """Contract for black-frame checker implementations."""

    @abstractmethod
    def is_black_frame(self, image: Image) -> bool:
        """Return `True` if the image is considered a black frame."""
        raise NotImplementedError
