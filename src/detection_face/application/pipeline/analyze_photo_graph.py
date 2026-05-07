"""Analyze photo graph."""

from __future__ import annotations

from time import perf_counter
from typing import TYPE_CHECKING, Any, Protocol, TypedDict, cast

from langgraph.graph import END, START, StateGraph

from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from detection_face.application.gateways.image_source import ImageSource
    from detection_face.application.gateways.prediction_writer import PredictionWriter
    from detection_face.application.gateways.run_logger import RunLogger
    from detection_face.application.use_cases.check_camera_health import (
        CheckCameraHealth,
    )
    from detection_face.domain.entities.camera_health_result import CameraHealthResult
    from detection_face.domain.entities.image import Image
else:
    Path = Any
    CameraHealthResult = Any
    Image = Any


class AnalyzePhotoState(TypedDict, total=False):
    """State passed through LangGraph nodes."""

    image_path: Path
    image: Image
    camera_health: CameraHealthResult
    result: AnalyzePhotoResult
    health_ms: float
    total_ms: float
    start_ts: float


class MermaidDrawable(Protocol):
    """Protocol describing objects that can export Mermaid diagrams."""

    def draw_mermaid(self) -> str:
        """Return graph rendered as Mermaid syntax."""


class CompiledAnalyzePhotoGraph(Protocol):
    """Protocol for the compiled graph interface used by the pipeline."""

    def invoke(self, state: dict[str, Path]) -> dict[str, object]:
        """Run the graph for a single execution."""

    def get_graph(self) -> MermaidDrawable:
        """Return a graph object with Mermaid export."""


def _build_start_node() -> Callable[[AnalyzePhotoState], AnalyzePhotoState]:
    """Create the start node for a new run."""

    def _start_node(_: AnalyzePhotoState) -> AnalyzePhotoState:
        return {"start_ts": perf_counter()}

    return _start_node


def _build_load_node(
    source: ImageSource,
) -> Callable[[AnalyzePhotoState], AnalyzePhotoState]:
    """Create the load-image node."""

    def _load_image(state: AnalyzePhotoState) -> AnalyzePhotoState:
        image = source.load(state["image_path"])
        return {"image": image}

    return _load_image


def _build_health_node(
    check_camera_health: CheckCameraHealth,
) -> Callable[[AnalyzePhotoState], AnalyzePhotoState]:
    """Create the health node."""

    def _check_health(
        state: AnalyzePhotoState,
    ) -> AnalyzePhotoState:
        started = perf_counter()
        health = check_camera_health.execute(state["image"])
        return {
            "camera_health": health,
            "health_ms": (perf_counter() - started) * 1000,
        }

    return _check_health


def _build_result_node() -> Callable[[AnalyzePhotoState], AnalyzePhotoState]:
    """Create the result aggregation node."""

    def _build_result(state: AnalyzePhotoState) -> AnalyzePhotoState:
        return {
            "result": AnalyzePhotoResult(
                camera_health=state["camera_health"],
            )
        }

    return _build_result


def _build_persist_node(
    writer: PredictionWriter,
    logger: RunLogger,
) -> Callable[[AnalyzePhotoState], AnalyzePhotoState]:
    """Create the persist-and-log node."""

    def _persist_and_log(state: AnalyzePhotoState) -> AnalyzePhotoState:
        image = state["image"]
        result = state["result"]
        writer.write(image, result)

        total_ms = 0.0
        if "start_ts" in state:
            total_ms = (perf_counter() - state["start_ts"]) * 1000

        logger.log(
            f"{image.path.name}: healthy={result.camera_health.is_healthy} "
            f"health={state['health_ms']:.2f}ms total={total_ms:.2f}ms"
        )
        return {"total_ms": total_ms}

    return _persist_and_log


def _add_node(
    builder: StateGraph[AnalyzePhotoState],
    name: str,
    node: Callable[[AnalyzePhotoState], AnalyzePhotoState],
) -> None:
    """Register a LangGraph node while preserving current graph typing."""
    builder.add_node(name, cast("Any", node))


def build_analyze_photo_graph(
    check_camera_health: CheckCameraHealth,
    source: ImageSource,
    writer: PredictionWriter,
    logger: RunLogger,
) -> CompiledAnalyzePhotoGraph:
    """Build and compile a linear LangGraph for image analysis."""
    builder: StateGraph[AnalyzePhotoState] = StateGraph(AnalyzePhotoState)
    _add_node(builder, "start", _build_start_node())
    _add_node(builder, "load", _build_load_node(source))
    _add_node(builder, "health", _build_health_node(check_camera_health))
    _add_node(builder, "result", _build_result_node())
    _add_node(builder, "persist", _build_persist_node(writer, logger))

    builder.add_edge(START, "start")
    builder.add_edge("start", "load")
    builder.add_edge("load", "health")
    builder.add_edge("health", "result")
    builder.add_edge("result", "persist")
    builder.add_edge("persist", END)

    return cast("CompiledAnalyzePhotoGraph", builder.compile())
