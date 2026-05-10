from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location_ping import LocationPing
from app.repositories.base import BaseRepository


class LocationRepository(BaseRepository[LocationPing]):
    model = LocationPing

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_latest_for_trip(self, trip_id: UUID) -> LocationPing | None:
        result = await self.db.execute(
            select(LocationPing)
            .where(LocationPing.trip_id == trip_id)
            .order_by(LocationPing.created_at.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def get_recent_for_trip(self, trip_id: UUID, limit: int = 10) -> list[LocationPing]:
        result = await self.db.execute(
            select(LocationPing)
            .where(LocationPing.trip_id == trip_id)
            .order_by(LocationPing.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
