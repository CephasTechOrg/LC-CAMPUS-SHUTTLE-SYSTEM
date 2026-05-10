from __future__ import annotations


class NotificationService:
    """Notification placeholder.

    The production version should integrate Firebase Cloud Messaging.

    This class is intentionally separated now so notification triggers can be added
    without mixing FCM logic into trip/location services.
    """

    async def notify_shuttle_started(self, trip_id: str) -> None:
        return None

    async def notify_shuttle_delayed(self, trip_id: str, reason: str) -> None:
        return None

    async def notify_shuttle_cancelled(self, trip_id: str, reason: str) -> None:
        return None

    async def notify_shuttle_near_stop(self, trip_id: str, stop_id: str) -> None:
        return None
