"""Filesystem run logger adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from detection_face.application.gateways.run_logger import RunLogger

if TYPE_CHECKING:
    from pathlib import Path


class FilesystemRunLogger(RunLogger):
    """Logs run messages to a file."""

    def __init__(self, log_path: Path) -> None:
        """Initialize and configure file logging.

        Args:
            log_path: Path to the log file.
        """
        log_path.parent.mkdir(parents=True, exist_ok=True)
        logger.add(
            log_path, level="INFO", format="{time} {level} {message}", rotation="10 MB"
        )

    def log(self, message: str) -> None:
        """Log a message.

        Args:
            message: Message to log.
        """
        logger.info(message)
