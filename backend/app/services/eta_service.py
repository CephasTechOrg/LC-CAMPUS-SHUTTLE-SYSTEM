from __future__ import annotations

from app.core.config import settings
from app.models.location_ping import LocationPing
from app.models.stop import Stop
from app.utils.geo import average, calculate_speed_mph, haversine_distance_miles, is_plausible_speed


class ETAService:
    """ETA and speed-calculation service.

    MVP algorithm:
        ETA = straight-line distance to next stop / average speed

    Production upgrade path:
        Replace straight-line distance with OSRM, Mapbox Directions, or Google Routes.
    """

    def distance_to_stop_miles(
        self,
        latitude: float,
        longitude: float,
        stop: Stop,
    ) -> float:
        return haversine_distance_miles(latitude, longitude, stop.latitude, stop.longitude)

    def estimate_eta_minutes(
        self,
        distance_miles: float,
        speed_mph: float | None,
    ) -> int | None:
        safe_speed = speed_mph or settings.DEFAULT_AVERAGE_SPEED_MPH
        if safe_speed <= 0:
            safe_speed = settings.DEFAULT_AVERAGE_SPEED_MPH

        hours = distance_miles / safe_speed
        minutes = round(hours * 60)

        return max(minutes, 1) if distance_miles > 0 else 0

    def compute_speed_from_previous_ping(
        self,
        previous: LocationPing | None,
        latitude: float,
        longitude: float,
        elapsed_seconds: float | None,
    ) -> float | None:
        if not previous or elapsed_seconds is None:
            return None

        calculated = calculate_speed_mph(
            previous_lat=previous.latitude,
            previous_lon=previous.longitude,
            current_lat=latitude,
            current_lon=longitude,
            elapsed_seconds=elapsed_seconds,
        )

        if is_plausible_speed(
            calculated,
            settings.MIN_VALID_SPEED_MPH,
            settings.MAX_VALID_SPEED_MPH,
        ):
            return calculated

        return None

    def choose_reliable_speed(
        self,
        phone_speed_mph: float | None,
        calculated_speed_mph: float | None,
        speed_samples: list[float],
    ) -> float:
        valid_samples = [
            speed
            for speed in speed_samples
            if is_plausible_speed(
                speed,
                settings.MIN_VALID_SPEED_MPH,
                settings.MAX_VALID_SPEED_MPH,
            )
        ]

        if is_plausible_speed(
            phone_speed_mph,
            settings.MIN_VALID_SPEED_MPH,
            settings.MAX_VALID_SPEED_MPH,
        ):
            valid_samples.append(float(phone_speed_mph))

        if is_plausible_speed(
            calculated_speed_mph,
            settings.MIN_VALID_SPEED_MPH,
            settings.MAX_VALID_SPEED_MPH,
        ):
            valid_samples.append(float(calculated_speed_mph))

        smoothed = average(valid_samples[-settings.SPEED_SAMPLE_SIZE :])
        return smoothed or settings.DEFAULT_AVERAGE_SPEED_MPH
