from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class LocationPingCreate(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    speed_mph: float | None = Field(default=None, ge=0)
    heading: float | None = Field(default=None, ge=0, le=360)


class LocationPingRead(BaseReadSchema):
    id: UUID
    trip_id: UUID
    shuttle_id: UUID
    latitude: float
    longitude: float
    speed_mph: float | None = None
    heading: float | None = None
    created_at: datetime


class StopSnapshot(BaseModel):
    id: UUID
    name: str
    latitude: float
    longitude: float


class ShuttleSnapshot(BaseModel):
    id: UUID
    name: str


class LiveTripResponse(BaseModel):
    trip_id: UUID
    route_id: UUID
    shuttle: ShuttleSnapshot
    status: str
    latitude: float | None = None
    longitude: float | None = None
    speed_mph: float | None = None
    heading: float | None = None
    next_stop: StopSnapshot | None = None
    eta_minutes: int | None = None
    distance_to_next_stop_miles: float | None = None
    last_updated: datetime | None = None
    is_location_stale: bool = False
    is_offline: bool = False
