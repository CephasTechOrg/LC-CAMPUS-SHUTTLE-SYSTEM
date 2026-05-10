from __future__ import annotations

from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.common import BaseReadSchema


class TimetableEntryCreate(BaseModel):
    route_id: UUID
    shuttle_id: UUID | None = None
    day_of_week: int = Field(ge=0, le=6)
    scheduled_start_time: time
    scheduled_end_time: time | None = None


class TimetableEntryRead(BaseReadSchema):
    id: UUID
    route_id: UUID
    shuttle_id: UUID | None = None
    day_of_week: int
    scheduled_start_time: time
    scheduled_end_time: time | None = None
    is_active: bool
    created_at: datetime
