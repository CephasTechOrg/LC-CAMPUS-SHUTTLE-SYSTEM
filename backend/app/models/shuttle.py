from __future__ import annotations

from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Shuttle(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "shuttles"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    plate_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="inactive", nullable=False)

    __table_args__ = (
        CheckConstraint(
            "status IN ('inactive', 'active', 'maintenance', 'offline')",
            name="ck_shuttles_status",
        ),
    )
