"""Analyze photo pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pathlib import Path

    from langgraph.graph.state import CompiledStateGraph
    from langgraph.types import GraphOutput

    from detection_face.application.gateways.image_source import ImageSource
    from detection_face.application.gateways.prediction_writer import PredictionWriter
    from detection_face.application.gateways.run_logger import RunLogger
    from detection_face.application.use_cases.check_camera_health import (
        CheckCameraHealth,
    )
    from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult

from detection_face.application.pipeline.analyze_photo_graph import (
    AnalyzePhotoState,
    build_analyze_photo_graph,
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
        self._graph: CompiledStateGraph[
            AnalyzePhotoState, None, AnalyzePhotoState, AnalyzePhotoState
        ] = build_analyze_photo_graph(
            check_camera_health=self._check_camera_health,
            source=self._source,
            writer=self._writer,
            logger=self._logger,
        )

    def run(self, path: Path) -> AnalyzePhotoResult:
        """Run the pipeline on a single image.

        Args:
            path: Path to the image file.

        Returns:
            Aggregated photo analysis result.
        """
        state = cast(
            "GraphOutput[AnalyzePhotoState]",
            self._graph.invoke({"image_path": path}, version="v2"),
        )
        return cast("AnalyzePhotoResult", state.value["result"])

    def mermaid(self) -> str:
        """Return the graph in Mermaid format.

        Returns:
            Mermaid text describing the graph.
        """
        return cast("str", self._graph.get_graph().draw_mermaid())

    def save_graph(self, path: Path) -> None:
        """Save the graph diagram.

        Args:
            path: Target file path for the Mermaid file.
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.mermaid())
