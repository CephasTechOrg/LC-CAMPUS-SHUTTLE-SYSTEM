from __future__ import annotations

from datetime import time
from uuid import UUID

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class TimetableEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "timetable_entries"

    route_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    shuttle_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("shuttles.id", ondelete="SET NULL"),
        nullable=True,
    )
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    scheduled_start_time: Mapped[time] = mapped_column(Time, nullable=False)
    scheduled_end_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        CheckConstraint("day_of_week BETWEEN 0 AND 6", name="ck_timetable_day_of_week"),
    )
