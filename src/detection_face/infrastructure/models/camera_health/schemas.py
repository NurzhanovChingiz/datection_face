"""Camera health schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class CameraHealthResultSchema(BaseModel):
    """Schema for the result of a camera health check."""

    is_black: bool = Field(..., description="Whether the image is black.")
