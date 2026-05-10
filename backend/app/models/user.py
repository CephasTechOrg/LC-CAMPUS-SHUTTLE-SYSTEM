from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin, UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.driver import Driver
    from app.models.stop import Stop


class User(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    preferred_stop_id: Mapped[UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stops.id", ondelete="SET NULL"),
        nullable=True,
    )

    preferred_stop: Mapped["Stop | None"] = relationship("Stop")
    driver_profile: Mapped["Driver | None"] = relationship(
        "Driver",
        back_populates="user",
        uselist=False,
    )

    __table_args__ = (
        CheckConstraint("role IN ('student', 'driver', 'admin')", name="ck_users_role"),
    )
