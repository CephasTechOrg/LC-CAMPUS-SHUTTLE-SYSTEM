from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import TripStatus
from app.db.redis import RedisClient
from app.repositories.trip_repository import TripRepository
from app.services.live_state_service import LiveStateService


class StaleDetectionService:
    def __init__(self, db: AsyncSession, redis: RedisClient):
        self.db = db
        self.redis = redis
        self.trips = TripRepository(db)
        self.live_state = LiveStateService(redis)

    async def get_live_response(self, trip_id: UUID):
        live = await self.live_state.get_live_state(trip_id)
        if not live:
            return None

        response = self.live_state.to_response(live)

        if response.is_offline:
            trip = await self.trips.get(trip_id)
            if trip and trip.status not in {TripStatus.COMPLETED.value, TripStatus.CANCELLED.value}:
                trip.status = TripStatus.OFFLINE.value
                await self.db.commit()

        return response
