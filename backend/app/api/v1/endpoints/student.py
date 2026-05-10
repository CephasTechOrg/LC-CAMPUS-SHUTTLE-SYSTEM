from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis
from app.db.redis import RedisClient
from app.repositories.trip_repository import TripRepository
from app.schemas.location import LiveTripResponse
from app.services.live_state_service import LiveStateService
from app.services.stale_detection_service import StaleDetectionService

router = APIRouter()


@router.get("/shuttles/active", response_model=list[LiveTripResponse])
async def get_active_shuttles(
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
):
    live_service = LiveStateService(redis)
    stale_service = StaleDetectionService(db, redis)

    trip_ids = await live_service.list_active_trip_ids()

    # Fallback to database if Redis was cleared but trips are active.
    if not trip_ids:
        active_trips = await TripRepository(db).list_active()
        trip_ids = {str(trip.id) for trip in active_trips}

    responses: list[LiveTripResponse] = []
    for trip_id in trip_ids:
        response = await stale_service.get_live_response(UUID(str(trip_id)))
        if response:
            responses.append(response)

    return responses


@router.get("/trips/{trip_id}/live", response_model=LiveTripResponse)
async def get_live_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
):
    response = await StaleDetectionService(db, redis).get_live_response(trip_id)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Live trip state not found.",
        )
    return response
