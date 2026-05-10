from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import TripStatus
from app.schemas.common import BaseReadSchema


class TripStartRequest(BaseModel):
    route_id: UUID
    shuttle_id: UUID
    scheduled_start_time: datetime | None = None
    next_stop_id: UUID | None = None


class ChangeNextStopRequest(BaseModel):
    next_stop_id: UUID


class DelayTripRequest(BaseModel):
    reason: str = Field(min_length=2, max_length=500)


class CancelTripRequest(BaseModel):
    reason: str = Field(min_length=2, max_length=500)


class TripRead(BaseReadSchema):
    id: UUID
    route_id: UUID
    shuttle_id: UUID
    driver_id: UUID
    scheduled_start_time: datetime | None = None
    actual_start_time: datetime | None = None
    actual_end_time: datetime | None = None
    current_stop_id: UUID | None = None
    next_stop_id: UUID | None = None
    status: str
    delay_reason: str | None = None
    cancellation_reason: str | None = None
    created_at: datetime


class TripStatusUpdate(BaseModel):
    status: TripStatus
