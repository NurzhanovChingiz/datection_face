"""CLI command for analyzing photos."""

from __future__ import annotations

import argparse
from pathlib import Path

from detection_face.composition import build_pipeline, next_version
from detection_face.infrastructure.config.yaml_loader import (
    load_camera_health_config,
    load_global_config,
)

_GLOBAL_CONFIG_PATH = Path("configs/global.yaml")
_CAMERA_HEALTH_CONFIG_PATH = Path("configs/camera_health.yaml")


def main() -> None:
    """Run the analyze photo pipeline on one or more images."""
    parser = argparse.ArgumentParser(description="Analyze photos for camera health.")
    parser.add_argument(
        "images",
        nargs="+",
        type=Path,
        help="Image file paths to analyze.",
    )
    parser.add_argument(
        "--global-config",
        type=Path,
        default=_GLOBAL_CONFIG_PATH,
        help="Path to global.yaml config.",
    )
    parser.add_argument(
        "--camera-health-config",
        type=Path,
        default=_CAMERA_HEALTH_CONFIG_PATH,
        help="Path to camera_health.yaml config.",
    )

    args = parser.parse_args()

    global_cfg = load_global_config(args.global_config)
    camera_health_cfg = load_camera_health_config(args.camera_health_config)
    version = next_version(global_cfg.artifacts_dir)
    run_dir = global_cfg.artifacts_dir / version
    pipeline = build_pipeline(
        global_cfg,
        camera_health_cfg,
        run_dir,
    )

    for image_path in args.images:
        result = pipeline.run(image_path)
        health = result.camera_health
        status = "healthy" if health.is_healthy else "unhealthy"
        print(  # noqa: T201
            f"{image_path.name}: {status} | black={health.is_black} "
        )
