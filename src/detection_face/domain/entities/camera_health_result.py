"""CameraHealthResult is a domain entity that represents the result of a camera health check."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraHealthResult:
    """Result of a camera health check."""

    is_black: bool

    @property
    def is_healthy(self) -> bool:
        """Return True if none of the health checks failed."""
        return not self.is_black
