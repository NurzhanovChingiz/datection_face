"""Image entity."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Image(ABC):
    """Image entity."""

    path: str
    face_detected: bool
    confidence: float

    @abstractmethod
    def get_path(self) -> str:
        """Get the path of the image."""
        return self.path

    @abstractmethod
    def get_face_detected(self) -> bool:
        """Get the face detected."""
        return self.face_detected

    @abstractmethod
    def get_confidence(self) -> float:
        """Get the confidence."""
        return self.confidence
