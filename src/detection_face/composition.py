"""Composition root."""

from __future__ import annotations

from typing import TYPE_CHECKING

from detection_face.application.pipeline.analyze_photo_pipeline import (
    AnalyzePhotoPipeline,
)
from detection_face.application.use_cases.check_camera_health import CheckCameraHealth
from detection_face.infrastructure.io.image_reader import CVImageReader
from detection_face.infrastructure.logging.filesystem_run_logger import (
    FilesystemRunLogger,
)
from detection_face.infrastructure.models.camera_health.black_image import (
    CVBlackImageChecker,
)
from detection_face.infrastructure.storage.filesystem_prediction_writer import (
    FilesystemPredictionWriter,
)

if TYPE_CHECKING:
    from pathlib import Path

    from detection_face.infrastructure.config.yaml_loader import (
        CameraHealthConfig,
        GlobalConfig,
    )


def next_version(artifacts_dir: Path) -> str:
    """Return the next auto-incremented version folder name.

    Scans for existing version_N folders and returns version_(N+1).
    Returns version_1 if none exist.

    Args:
        artifacts_dir: Base directory that contains version folders.

    Returns:
        Next version string, e.g. 'version_3'.
    """
    if not artifacts_dir.exists():
        return "version_1"
    numbers = [
        int(d.name.split("_")[1])
        for d in artifacts_dir.iterdir()
        if d.is_dir()
        and d.name.startswith("version_")
        and d.name.split("_")[1].isdigit()
    ]
    return f"version_{max(numbers) + 1}" if numbers else "version_1"


def build_pipeline(
    global_config: GlobalConfig,
    camera_health_config: CameraHealthConfig,
    run_dir: Path,
) -> AnalyzePhotoPipeline:
    """Build the analyze photo pipeline from configs and run directory.

    Args:
        global_config: Frozen global configuration.
        camera_health_config: Frozen camera health configuration.
        run_dir: Root directory for this run's outputs (artifacts/runs/<version>/<run_id>).

    Returns:
        Fully wired AnalyzePhotoPipeline instance.
    """
    _ = global_config

    check_camera_health = CheckCameraHealth(
        black=CVBlackImageChecker(threshold=camera_health_config.black_threshold),
    )

    return AnalyzePhotoPipeline(
        check_camera_health=check_camera_health,
        source=CVImageReader(),
        writer=FilesystemPredictionWriter(output_dir=run_dir / "predictions" / "json"),
        logger=FilesystemRunLogger(log_path=run_dir / "logs" / "inference.log"),
    )
