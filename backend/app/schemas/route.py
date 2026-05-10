from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema
from app.schemas.stop import StopRead


class RouteCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None


class RouteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    is_active: bool | None = None


class RouteRead(BaseReadSchema):
    id: UUID
    name: str
    description: str | None = None
    is_active: bool
    created_at: datetime


class RouteStopCreate(BaseModel):
    stop_id: UUID
    stop_order: int = Field(ge=1)
    estimated_minutes_from_previous: int | None = Field(default=None, ge=0)


class RouteStopRead(BaseReadSchema):
    id: UUID
    route_id: UUID
    stop_id: UUID
    stop_order: int
    estimated_minutes_from_previous: int | None = None
    stop: StopRead | None = None
