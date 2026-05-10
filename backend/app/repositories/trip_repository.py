from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.constants import ACTIVE_TRIP_STATUSES
from app.models.trip import Trip
from app.repositories.base import BaseRepository


class TripRepository(BaseRepository[Trip]):
    model = Trip

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_with_relations(self, trip_id: UUID) -> Trip | None:
        result = await self.db.execute(
            select(Trip)
            .options(
                selectinload(Trip.shuttle),
                selectinload(Trip.next_stop),
                selectinload(Trip.route),
                selectinload(Trip.driver),
            )
            .where(Trip.id == trip_id)
        )
        return result.scalar_one_or_none()

    async def get_active_by_shuttle(self, shuttle_id: UUID) -> Trip | None:
        active_values = [status.value for status in ACTIVE_TRIP_STATUSES]
        result = await self.db.execute(
            select(Trip)
            .where(Trip.shuttle_id == shuttle_id, Trip.status.in_(active_values))
            .order_by(Trip.actual_start_time.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_active(self) -> list[Trip]:
        active_values = [status.value for status in ACTIVE_TRIP_STATUSES]
        result = await self.db.execute(
            select(Trip)
            .options(selectinload(Trip.shuttle), selectinload(Trip.next_stop))
            .where(Trip.status.in_(active_values))
            .order_by(Trip.actual_start_time.desc())
        )
        return list(result.scalars().all())
