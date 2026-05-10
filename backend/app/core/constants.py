from __future__ import annotations

from enum import StrEnum


class UserRole(StrEnum):
    STUDENT = "student"
    DRIVER = "driver"
    ADMIN = "admin"


class TripStatus(StrEnum):
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    DELAYED = "delayed"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OFFLINE = "offline"


class ShuttleStatus(StrEnum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


ACTIVE_TRIP_STATUSES = {
    TripStatus.ACTIVE,
    TripStatus.DELAYED,
    TripStatus.PAUSED,
    TripStatus.OFFLINE,
}
