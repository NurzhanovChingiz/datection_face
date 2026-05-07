"""Analyze photo pipeline."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, cast

from detection_face.application.pipeline.analyze_photo_graph import (
    CompiledAnalyzePhotoGraph,
    build_analyze_photo_graph,
)

if TYPE_CHECKING:
    from pathlib import Path

    from detection_face.application.gateways.image_source import ImageSource
    from detection_face.application.gateways.prediction_writer import PredictionWriter
    from detection_face.application.gateways.run_logger import RunLogger
    from detection_face.application.use_cases.check_camera_health import (
        CheckCameraHealth,
    )
    from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult


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
        self._graph: CompiledAnalyzePhotoGraph = build_analyze_photo_graph(
            check_camera_health=check_camera_health,
            source=source,
            writer=writer,
            logger=logger,
        )

    def run(self, path: Path) -> AnalyzePhotoResult:
        """Run the pipeline on a single image using LangGraph.

        Args:
            path: Path to the image file.

        Returns:
            Aggregated photo analysis result.
        """
        graph_result = self._graph.invoke({"image_path": path})
        return cast("AnalyzePhotoResult", graph_result["result"])

    def save_graph(self, output_path: Path) -> None:
        """Save Mermaid graph to file.

        Args:
            output_path: File path where the Mermaid graph is written.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        graph = self._graph.get_graph()
        output_path.write_text(graph.draw_mermaid())
