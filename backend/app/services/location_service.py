from __future__ import annotations

from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import ACTIVE_TRIP_STATUSES, TripStatus
from app.db.redis import RedisClient
from app.models.location_ping import LocationPing
from app.repositories.location_repository import LocationRepository
from app.repositories.stop_repository import StopRepository
from app.repositories.trip_repository import TripRepository
from app.schemas.location import LiveTripResponse, LocationPingCreate
from app.services.eta_service import ETAService
from app.services.live_state_service import LiveStateService
from app.utils.time import seconds_since, utc_now


class LocationService:
    def __init__(self, db: AsyncSession, redis: RedisClient):
        self.db = db
        self.redis = redis
        self.trips = TripRepository(db)
        self.locations = LocationRepository(db)
        self.stops = StopRepository(db)
        self.eta = ETAService()
        self.live_state = LiveStateService(redis)

    async def process_location_ping(
        self,
        trip_id: UUID,
        driver_id: UUID,
        payload: LocationPingCreate,
    ) -> LiveTripResponse:
        trip = await self.trips.get_with_relations(trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found.")

        if trip.driver_id != driver_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This trip does not belong to you.")

        if trip.status not in {status.value for status in ACTIVE_TRIP_STATUSES}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Cannot send location for trip with status '{trip.status}'.",
            )

        previous_ping = await self.locations.get_latest_for_trip(trip_id)
        elapsed = seconds_since(previous_ping.created_at) if previous_ping else None

        calculated_speed = self.eta.compute_speed_from_previous_ping(
            previous=previous_ping,
            latitude=payload.latitude,
            longitude=payload.longitude,
            elapsed_seconds=elapsed,
        )

        existing_samples = await self.live_state.get_speed_samples(trip_id)
        reliable_speed = self.eta.choose_reliable_speed(
            phone_speed_mph=payload.speed_mph,
            calculated_speed_mph=calculated_speed,
            speed_samples=existing_samples,
        )

        new_samples = existing_samples + [reliable_speed]
        await self.live_state.save_speed_samples(trip_id, new_samples)

        ping = LocationPing(
            trip_id=trip.id,
            shuttle_id=trip.shuttle_id,
            latitude=payload.latitude,
            longitude=payload.longitude,
            speed_mph=reliable_speed,
            heading=payload.heading,
        )
        await self.locations.add(ping)

        if trip.status == TripStatus.OFFLINE.value:
            trip.status = TripStatus.ACTIVE.value

        next_stop = trip.next_stop
        distance_miles = None
        eta_minutes = None
        next_stop_state = None

        if next_stop:
            distance_miles = self.eta.distance_to_stop_miles(
                latitude=payload.latitude,
                longitude=payload.longitude,
                stop=next_stop,
            )
            eta_minutes = self.eta.estimate_eta_minutes(distance_miles, reliable_speed)
            next_stop_state = {
                "id": str(next_stop.id),
                "name": next_stop.name,
                "latitude": next_stop.latitude,
                "longitude": next_stop.longitude,
            }

        now = utc_now()

        live_state = {
            "trip_id": str(trip.id),
            "route_id": str(trip.route_id),
            "shuttle": {
                "id": str(trip.shuttle.id),
                "name": trip.shuttle.name,
            },
            "status": trip.status,
            "latitude": payload.latitude,
            "longitude": payload.longitude,
            "speed_mph": reliable_speed,
            "heading": payload.heading,
            "next_stop": next_stop_state,
            "eta_minutes": eta_minutes,
            "distance_to_next_stop_miles": round(distance_miles, 3) if distance_miles is not None else None,
            "last_updated": now.isoformat(),
            "is_location_stale": False,
            "is_offline": False,
        }

        await self.live_state.save_live_state(live_state)
        await self.db.commit()

        return self.live_state.to_response(live_state)
