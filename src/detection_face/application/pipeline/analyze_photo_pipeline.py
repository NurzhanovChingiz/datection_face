"""Analyze photo pipeline."""

from __future__ import annotations

from time import perf_counter
from typing import TYPE_CHECKING

from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult

if TYPE_CHECKING:
    from pathlib import Path

    from detection_face.application.gateways.image_source import ImageSource
    from detection_face.application.gateways.prediction_writer import PredictionWriter
    from detection_face.application.gateways.run_logger import RunLogger
    from detection_face.application.use_cases.check_camera_health import (
        CheckCameraHealth,
    )


class AnalyzePhotoPipeline:
    """Analyze photo pipeline."""

    def __init__(
        self,
        check_camera_health: CheckCameraHealth,
        source: ImageSource,
        writer: PredictionWriter,
        logger: RunLogger,
    ) -> None:
        """Initialize the pipeline with its dependencies.

        Args:
            check_camera_health: Use case for checking camera health.
            source: Image source gateway.
            writer: Prediction writer gateway.
            logger: Run logger gateway.
        """
        self._check_camera_health = check_camera_health
        self._source = source
        self._writer = writer
        self._logger = logger

    def run(self, path: Path) -> AnalyzePhotoResult:
        """Run the pipeline on a single image.

        Logs per-stage and total latency in milliseconds. Per-stage timings
        cover only the three model executions; total covers the whole call.

        Args:
            path: Path to the image file.

        Returns:
            Aggregated photo analysis result.
        """
        start_time = perf_counter()
        image = self._source.load(path)

        health_start = perf_counter()
        camera_health = self._check_camera_health.execute(image)
        health_ms = (perf_counter() - health_start) * 1000

        result = AnalyzePhotoResult(
            camera_health=camera_health,
        )
        self._writer.write(image, result)
        total_ms = (perf_counter() - start_time) * 1000
        self._logger.log(
            f"{path.name}: healthy={camera_health.is_healthy} "
            f"health={health_ms:.2f}ms total={total_ms:.2f}ms",
        )
        return result
