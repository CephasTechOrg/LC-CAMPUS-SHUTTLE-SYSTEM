from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.core.constants import ShuttleStatus
from app.schemas.common import BaseReadSchema


class ShuttleCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    plate_number: str | None = Field(default=None, max_length=50)


class ShuttleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    plate_number: str | None = Field(default=None, max_length=50)
    status: ShuttleStatus | None = None


class ShuttleRead(BaseReadSchema):
    id: UUID
    name: str
    plate_number: str | None = None
    status: str
    created_at: datetime
