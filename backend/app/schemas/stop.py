from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class StopCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class StopUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    is_active: bool | None = None


class StopRead(BaseReadSchema):
    id: UUID
    name: str
    description: str | None = None
    latitude: float
    longitude: float
    is_active: bool
    created_at: datetime
