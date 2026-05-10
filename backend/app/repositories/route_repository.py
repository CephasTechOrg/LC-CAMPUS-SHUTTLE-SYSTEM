from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.route import Route
from app.models.route_stop import RouteStop
from app.repositories.base import BaseRepository


class RouteRepository(BaseRepository[Route]):
    model = Route

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_with_stops(self, route_id: UUID) -> Route | None:
        result = await self.db.execute(
            select(Route)
            .options(selectinload(Route.route_stops).selectinload(RouteStop.stop))
            .where(Route.id == route_id)
        )
        return result.scalar_one_or_none()

    async def get_first_route_stop(self, route_id: UUID) -> RouteStop | None:
        result = await self.db.execute(
            select(RouteStop)
            .where(RouteStop.route_id == route_id)
            .order_by(RouteStop.stop_order.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def add_route_stop(self, route_stop: RouteStop) -> RouteStop:
        self.db.add(route_stop)
        await self.db.flush()
        await self.db.refresh(route_stop)
        return route_stop
