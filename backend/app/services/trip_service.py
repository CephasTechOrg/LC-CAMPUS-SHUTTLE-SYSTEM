from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ShuttleStatus, TripStatus
from app.db.redis import RedisClient
from app.models.trip import Trip
from app.repositories.driver_repository import DriverRepository
from app.repositories.route_repository import RouteRepository
from app.repositories.shuttle_repository import ShuttleRepository
from app.repositories.stop_repository import StopRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripStartRequest
from app.services.live_state_service import LiveStateService
from app.utils.time import utc_now


class TripService:
    def __init__(self, db: AsyncSession, redis: RedisClient):
        self.db = db
        self.redis = redis
        self.trips = TripRepository(db)
        self.routes = RouteRepository(db)
        self.stops = StopRepository(db)
        self.shuttles = ShuttleRepository(db)
        self.drivers = DriverRepository(db)
        self.live_state = LiveStateService(redis)

    async def start_trip(self, driver_id: UUID, payload: TripStartRequest) -> Trip:
        route = await self.routes.get(payload.route_id)
        if not route or not route.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found or inactive.")

        shuttle = await self.shuttles.get(payload.shuttle_id)
        if not shuttle:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shuttle not found.")

        existing_active = await self.trips.get_active_by_shuttle(payload.shuttle_id)
        if existing_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This shuttle already has an active trip.",
            )

        next_stop_id = payload.next_stop_id
        if next_stop_id is None:
            first_route_stop = await self.routes.get_first_route_stop(payload.route_id)
            if not first_route_stop:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Route has no stops. Add stops before starting a trip.",
                )
            next_stop_id = first_route_stop.stop_id
        else:
            stop = await self.stops.get(next_stop_id)
            if not stop or not stop.is_active:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Next stop not found or inactive.")

        trip = Trip(
            route_id=payload.route_id,
            shuttle_id=payload.shuttle_id,
            driver_id=driver_id,
            scheduled_start_time=payload.scheduled_start_time,
            actual_start_time=utc_now(),
            next_stop_id=next_stop_id,
            status=TripStatus.ACTIVE.value,
        )

        shuttle.status = ShuttleStatus.ACTIVE.value

        await self.trips.add(trip)
        await self.db.commit()
        await self.db.refresh(trip)

        await self.live_state.save_live_state(
            {
                "trip_id": str(trip.id),
                "route_id": str(trip.route_id),
                "shuttle": {
                    "id": str(shuttle.id),
                    "name": shuttle.name,
                },
                "status": trip.status,
                "latitude": None,
                "longitude": None,
                "speed_mph": None,
                "heading": None,
                "next_stop": None,
                "eta_minutes": None,
                "distance_to_next_stop_miles": None,
                "last_updated": None,
                "is_location_stale": True,
                "is_offline": False,
            }
        )

        return trip

    async def end_trip(self, trip_id: UUID, driver_id: UUID) -> Trip:
        trip = await self.trips.get(trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")

        if trip.driver_id != driver_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This trip does not belong to you.")

        if trip.status in {TripStatus.COMPLETED.value, TripStatus.CANCELLED.value}:
            return trip

        trip.status = TripStatus.COMPLETED.value
        trip.actual_end_time = utc_now()

        shuttle = await self.shuttles.get(trip.shuttle_id)
        if shuttle:
            shuttle.status = ShuttleStatus.INACTIVE.value

        await self.db.commit()
        await self.live_state.remove_active_trip(trip.id)
        return trip

    async def change_next_stop(self, trip_id: UUID, driver_id: UUID, next_stop_id: UUID) -> Trip:
        trip = await self.trips.get(trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")

        if trip.driver_id != driver_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This trip does not belong to you.")

        stop = await self.stops.get(next_stop_id)
        if not stop or not stop.is_active:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found or inactive.")

        trip.next_stop_id = next_stop_id
        await self.db.commit()
        await self.db.refresh(trip)

        live = await self.live_state.get_live_state(trip.id)
        if live:
            live["next_stop"] = {
                "id": str(stop.id),
                "name": stop.name,
                "latitude": stop.latitude,
                "longitude": stop.longitude,
            }
            await self.live_state.save_live_state(live)

        return trip

    async def report_delay(self, trip_id: UUID, driver_id: UUID, reason: str) -> Trip:
        trip = await self.trips.get(trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")
        if trip.driver_id != driver_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This trip does not belong to you.")

        trip.status = TripStatus.DELAYED.value
        trip.delay_reason = reason
        await self.db.commit()
        await self.db.refresh(trip)
        return trip

    async def cancel_trip(self, trip_id: UUID, driver_id: UUID, reason: str) -> Trip:
        trip = await self.trips.get(trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")
        if trip.driver_id != driver_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This trip does not belong to you.")

        trip.status = TripStatus.CANCELLED.value
        trip.cancellation_reason = reason
        trip.actual_end_time = utc_now()

        shuttle = await self.shuttles.get(trip.shuttle_id)
        if shuttle:
            shuttle.status = ShuttleStatus.INACTIVE.value

        await self.db.commit()
        await self.live_state.remove_active_trip(trip.id)
        await self.db.refresh(trip)
        return trip
