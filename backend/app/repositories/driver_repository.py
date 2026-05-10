from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.driver import Driver
from app.repositories.base import BaseRepository


class DriverRepository(BaseRepository[Driver]):
    model = Driver

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_user_id(self, user_id: UUID) -> Driver | None:
        result = await self.db.execute(select(Driver).where(Driver.user_id == user_id))
        return result.scalar_one_or_none()
