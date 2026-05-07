"""Image domain entity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    import numpy as np


@dataclass(frozen=True)
class Image:
    """Image holding raw pixel data and its source path."""

    image_id: str
    path: Path
    data: np.ndarray = field(compare=False, hash=False, repr=False)
    shape: tuple[int, int, int] = field(compare=False, hash=False, repr=False)
