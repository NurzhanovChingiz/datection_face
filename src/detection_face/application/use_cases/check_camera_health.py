"""Check camera health use case."""

from __future__ import annotations

from typing import TYPE_CHECKING

from detection_face.domain.entities.camera_health_result import CameraHealthResult

if TYPE_CHECKING:
    from detection_face.domain.entities.image import Image
    from detection_face.domain.ports.black_image_checker import BlackImageChecker


class CheckCameraHealth:
    """Check camera health use case."""

    def __init__(
        self,
        black: BlackImageChecker,
    ) -> None:
        """Initialize with checker dependencies.

        Args:
            black: Black image checker.
            blur: Blur image checker.
        """
        self._black = black

    def execute(self, image: Image) -> CameraHealthResult:
        """Execute the camera health check.

        Args:
            image: The image to check.

        Returns:
            Camera health check result.
        """
        return CameraHealthResult(
            is_black=self._black.check(image),
        )
