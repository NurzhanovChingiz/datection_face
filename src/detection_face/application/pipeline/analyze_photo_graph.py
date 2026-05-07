"""LangGraph definition for analyze photo pipeline."""

from __future__ import annotations

from time import perf_counter
from typing import TYPE_CHECKING, TypedDict, cast

from langgraph.graph import END, START, StateGraph

from detection_face.domain.entities.analyze_photo_result import AnalyzePhotoResult

if TYPE_CHECKING:
    from pathlib import Path

    from langgraph.graph._node import StateNode
    from langgraph.graph.state import CompiledStateGraph

    from detection_face.application.gateways.image_source import ImageSource
    from detection_face.application.gateways.prediction_writer import PredictionWriter
    from detection_face.application.gateways.run_logger import RunLogger
    from detection_face.application.use_cases.check_camera_health import (
        CheckCameraHealth,
    )
    from detection_face.domain.entities.camera_health_result import CameraHealthResult
    from detection_face.domain.entities.image import Image


class AnalyzePhotoState(TypedDict, total=False):
    """State passed through LangGraph nodes."""

    image_path: Path
    image: Image
    camera_health: CameraHealthResult
    result: AnalyzePhotoResult
    health_ms: float
    total_ms: float
    start_ts: float


def _build_load_node(
    source: ImageSource,
) -> StateNode[AnalyzePhotoState]:
    def _load_image(state: AnalyzePhotoState) -> AnalyzePhotoState:
        image = source.load(state["image_path"])
        return {"image": image}

    return _load_image


def _build_health_node(
    check_camera_health: CheckCameraHealth,
) -> StateNode[AnalyzePhotoState]:
    def _check_health(state: AnalyzePhotoState) -> AnalyzePhotoState:
        started = perf_counter()
        health = check_camera_health.execute(state["image"])
        return {
            "camera_health": health,
            "health_ms": (perf_counter() - started) * 1000,
        }

    return _check_health


def _build_result_node() -> StateNode[AnalyzePhotoState]:
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
) -> StateNode[AnalyzePhotoState]:
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
        return {}

    return _persist_and_log


def build_analyze_photo_graph(
    check_camera_health: CheckCameraHealth,
    source: ImageSource,
    writer: PredictionWriter,
    logger: RunLogger,
) -> CompiledStateGraph[AnalyzePhotoState, None, AnalyzePhotoState, AnalyzePhotoState]:
    """Build and compile a linear LangGraph for deterministic image analysis."""

    def _start_node() -> StateNode[AnalyzePhotoState]:
        def _init(_state: AnalyzePhotoState) -> AnalyzePhotoState:
            return {"start_ts": perf_counter()}

        return cast("StateNode[AnalyzePhotoState]", _init)

    builder: StateGraph[
        AnalyzePhotoState, None, AnalyzePhotoState, AnalyzePhotoState
    ] = StateGraph(AnalyzePhotoState)
    builder.add_node("start", cast("StateNode[AnalyzePhotoState]", _start_node()))
    builder.add_node(
        "load", cast("StateNode[AnalyzePhotoState]", _build_load_node(source))
    )
    builder.add_node(
        "health",
        cast("StateNode[AnalyzePhotoState]", _build_health_node(check_camera_health)),
    )
    builder.add_node(
        "result", cast("StateNode[AnalyzePhotoState]", _build_result_node())
    )
    builder.add_node(
        "persist",
        cast("StateNode[AnalyzePhotoState]", _build_persist_node(writer, logger)),
    )

    builder.add_edge(START, "start")
    builder.add_edge("start", "load")
    builder.add_edge("load", "health")
    builder.add_edge("health", "result")
    builder.add_edge("result", "persist")
    builder.add_edge("persist", END)

    return builder.compile()
