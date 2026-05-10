from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis
from app.core.constants import UserRole
from app.core.permissions import require_roles
from app.db.redis import RedisClient
from app.models.user import User
from app.repositories.driver_repository import DriverRepository
from app.schemas.location import LiveTripResponse, LocationPingCreate
from app.schemas.trip import (
    CancelTripRequest,
    ChangeNextStopRequest,
    DelayTripRequest,
    TripRead,
    TripStartRequest,
)
from app.services.location_service import LocationService
from app.services.trip_service import TripService

router = APIRouter()


async def get_driver_id_for_user(db: AsyncSession, user: User) -> UUID:
    driver = await DriverRepository(db).get_by_user_id(user.id)
    if not driver or not driver.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Active driver profile not found for this user.",
        )
    return driver.id


@router.post("/trips/start", response_model=TripRead, status_code=201)
async def start_trip(
    payload: TripStartRequest,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await TripService(db, redis).start_trip(driver_id, payload)


@router.post("/trips/{trip_id}/location", response_model=LiveTripResponse)
async def send_location_ping(
    trip_id: UUID,
    payload: LocationPingCreate,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await LocationService(db, redis).process_location_ping(trip_id, driver_id, payload)


@router.patch("/trips/{trip_id}/next-stop", response_model=TripRead)
async def change_next_stop(
    trip_id: UUID,
    payload: ChangeNextStopRequest,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await TripService(db, redis).change_next_stop(trip_id, driver_id, payload.next_stop_id)


@router.patch("/trips/{trip_id}/delay", response_model=TripRead)
async def report_delay(
    trip_id: UUID,
    payload: DelayTripRequest,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await TripService(db, redis).report_delay(trip_id, driver_id, payload.reason)


@router.patch("/trips/{trip_id}/cancel", response_model=TripRead)
async def cancel_trip(
    trip_id: UUID,
    payload: CancelTripRequest,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await TripService(db, redis).cancel_trip(trip_id, driver_id, payload.reason)


@router.post("/trips/{trip_id}/end", response_model=TripRead)
async def end_trip(
    trip_id: UUID,
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
    current_user: User = Depends(require_roles(UserRole.DRIVER)),
):
    driver_id = await get_driver_id_for_user(db, current_user)
    return await TripService(db, redis).end_trip(trip_id, driver_id)
