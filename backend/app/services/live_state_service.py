from __future__ import annotations

from datetime import datetime
from uuid import UUID

from app.core.config import settings
from app.db.redis import RedisClient
from app.schemas.location import LiveTripResponse, ShuttleSnapshot, StopSnapshot
from app.utils.time import seconds_since

ACTIVE_TRIPS_KEY = "active_trips"


def live_trip_key(trip_id: UUID | str) -> str:
    return f"trip:{trip_id}:live"


def speed_samples_key(trip_id: UUID | str) -> str:
    return f"trip:{trip_id}:speed_samples"


class LiveStateService:
    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def save_live_state(self, state: dict) -> None:
        trip_id = str(state["trip_id"])
        await self.redis.set_json(
            live_trip_key(trip_id),
            state,
            expire_seconds=settings.LIVE_STATE_TTL_SECONDS,
        )
        await self.redis.sadd(ACTIVE_TRIPS_KEY, trip_id)

    async def get_live_state(self, trip_id: UUID | str) -> dict | None:
        return await self.redis.get_json(live_trip_key(trip_id))

    async def remove_active_trip(self, trip_id: UUID | str) -> None:
        await self.redis.srem(ACTIVE_TRIPS_KEY, str(trip_id))

    async def list_active_trip_ids(self) -> set[str]:
        return await self.redis.smembers(ACTIVE_TRIPS_KEY)

    async def get_speed_samples(self, trip_id: UUID | str) -> list[float]:
        values = await self.redis.get_json(speed_samples_key(trip_id))
        if not values:
            return []
        return [float(value) for value in values]

    async def save_speed_samples(self, trip_id: UUID | str, samples: list[float]) -> None:
        await self.redis.set_json(
            speed_samples_key(trip_id),
            samples[-settings.SPEED_SAMPLE_SIZE :],
            expire_seconds=settings.LIVE_STATE_TTL_SECONDS,
        )

    def apply_stale_flags(self, state: dict) -> dict:
        last_ping = state.get("last_updated")
        if isinstance(last_ping, str):
            last_ping_dt = datetime.fromisoformat(last_ping.replace("Z", "+00:00"))
        else:
            last_ping_dt = last_ping

        age = seconds_since(last_ping_dt)
        if age is None:
            state["is_location_stale"] = True
            state["is_offline"] = True
            state["status"] = "offline"
            return state

        state["is_location_stale"] = age > settings.STALE_LOCATION_SECONDS
        state["is_offline"] = age > settings.OFFLINE_LOCATION_SECONDS
        if state["is_offline"] and state.get("status") not in {"completed", "cancelled"}:
            state["status"] = "offline"

        return state

    def to_response(self, state: dict) -> LiveTripResponse:
        state = self.apply_stale_flags(state)

        shuttle_data = state["shuttle"]
        next_stop_data = state.get("next_stop")

        return LiveTripResponse(
            trip_id=UUID(str(state["trip_id"])),
            route_id=UUID(str(state["route_id"])),
            shuttle=ShuttleSnapshot(
                id=UUID(str(shuttle_data["id"])),
                name=shuttle_data["name"],
            ),
            status=state["status"],
            latitude=state.get("latitude"),
            longitude=state.get("longitude"),
            speed_mph=state.get("speed_mph"),
            heading=state.get("heading"),
            next_stop=(
                StopSnapshot(
                    id=UUID(str(next_stop_data["id"])),
                    name=next_stop_data["name"],
                    latitude=next_stop_data["latitude"],
                    longitude=next_stop_data["longitude"],
                )
                if next_stop_data
                else None
            ),
            eta_minutes=state.get("eta_minutes"),
            distance_to_next_stop_miles=state.get("distance_to_next_stop_miles"),
            last_updated=(
                datetime.fromisoformat(state["last_updated"].replace("Z", "+00:00"))
                if isinstance(state.get("last_updated"), str)
                else state.get("last_updated")
            ),
            is_location_stale=state["is_location_stale"],
            is_offline=state["is_offline"],
        )
