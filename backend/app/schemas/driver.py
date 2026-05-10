from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.schemas.common import BaseReadSchema


class DriverCreate(BaseModel):
    user_id: UUID
    assigned_shuttle_id: UUID | None = None


class DriverRead(BaseReadSchema):
    id: UUID
    user_id: UUID
    assigned_shuttle_id: UUID | None = None
    is_active: bool
    created_at: datetime
