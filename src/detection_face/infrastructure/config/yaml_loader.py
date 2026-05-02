"""YAML config loader."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class GlobalConfig:
    """Frozen global config shared across all tasks."""

    artifacts_dir: Path
    log_level: str


@dataclass(frozen=True)
class CameraHealthConfig:
    """Frozen config for the camera health task."""

    black_threshold: float


def load_global_config(path: Path) -> GlobalConfig:
    """Load global config from YAML.

    Args:
        path: Path to the global YAML config file.

    Returns:
        Frozen GlobalConfig instance.
    """
    raw = yaml.safe_load(path.read_text())
    return GlobalConfig(
        artifacts_dir=Path(raw["artifacts_dir"]),
        log_level=raw["log_level"],
    )


def load_camera_health_config(path: Path) -> CameraHealthConfig:
    """Load camera health config from YAML.

    Args:
        path: Path to the YAML config file.

    Returns:
        Frozen CameraHealthConfig instance.
    """
    raw = yaml.safe_load(path.read_text())
    return CameraHealthConfig(
        black_threshold=raw["black_threshold"],
    )
