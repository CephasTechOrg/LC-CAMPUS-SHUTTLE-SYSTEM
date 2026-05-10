from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import EmailStr

from app.schemas.common import BaseReadSchema


class UserRead(BaseReadSchema):
    id: UUID
    name: str
    email: EmailStr
    role: str
    preferred_stop_id: UUID | None = None
    created_at: datetime
