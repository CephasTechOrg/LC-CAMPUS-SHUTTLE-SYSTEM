from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.timetable import TimetableEntry
from app.repositories.base import BaseRepository


class TimetableRepository(BaseRepository[TimetableEntry]):
    model = TimetableEntry

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def list_active(self) -> list[TimetableEntry]:
        result = await self.db.execute(
            select(TimetableEntry)
            .where(TimetableEntry.is_active.is_(True))
            .order_by(TimetableEntry.day_of_week.asc(), TimetableEntry.scheduled_start_time.asc())
        )
        return list(result.scalars().all())
