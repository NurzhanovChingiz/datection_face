"""RunLogger gateway — logs run messages."""

from __future__ import annotations

from abc import ABC, abstractmethod


class RunLogger(ABC):
    """Abstract base for run logger."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Log a message.

        Args:
            message: Message to log.
        """
