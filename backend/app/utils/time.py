from __future__ import annotations

from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def ensure_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def seconds_since(value: datetime | None) -> float | None:
    if value is None:
        return None
    return (utc_now() - ensure_aware_utc(value)).total_seconds()
