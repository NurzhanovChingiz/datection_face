"""Filesystem prediction writer adapter."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import TYPE_CHECKING

from detection_face.application.gateways.prediction_writer import PredictionWriter

if TYPE_CHECKING:
    from pathlib import Path

    from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult
    from detection_face.domain.entities.image import Image


class FilesystemPredictionWriter(PredictionWriter):
    """Writes prediction results as JSON to the filesystem."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize with output directory.

        Args:
            output_dir: Directory where JSON results are written.
        """
        self._output_dir = output_dir

    def write(self, image: Image, result: AnalyzePhotoResult) -> None:
        """Write prediction result to JSON file.

        Args:
            image: Source image.
            result: Aggregated photo analysis result.
        """
        self._output_dir.mkdir(parents=True, exist_ok=True)
        out = self._output_dir / f"{image.path.stem}.json"
        prediction = {
            "image": {
                "image_id": image.image_id,
                "path": str(image.path),
                "shape": image.shape,
            },
            **asdict(result),
        }
        out.write_text(json.dumps(prediction, indent=2))
