from __future__ import annotations

from math import atan2, cos, radians, sin, sqrt

EARTH_RADIUS_MILES = 3958.7613


def haversine_distance_miles(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Return straight-line distance in miles between two lat/lon points.

    This is intentionally lightweight for the MVP. Later, replace or supplement this
    with road-network distance from OSRM, Mapbox Directions, or Google Routes.
    """
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = sin(dlat / 2) ** 2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_MILES * c


def calculate_speed_mph(
    previous_lat: float,
    previous_lon: float,
    current_lat: float,
    current_lon: float,
    elapsed_seconds: float,
) -> float | None:
    if elapsed_seconds <= 0:
        return None

    distance_miles = haversine_distance_miles(
        previous_lat,
        previous_lon,
        current_lat,
        current_lon,
    )
    hours = elapsed_seconds / 3600
    if hours <= 0:
        return None

    return distance_miles / hours


def is_plausible_speed(speed_mph: float | None, min_speed: float, max_speed: float) -> bool:
    if speed_mph is None:
        return False
    return min_speed <= speed_mph <= max_speed


def average(values: list[float]) -> float | None:
    clean = [value for value in values if value is not None]
    if not clean:
        return None
    return sum(clean) / len(clean)
