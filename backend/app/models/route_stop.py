from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import UUIDPrimaryKeyMixin

if TYPE_CHECKING:
    from app.models.route import Route
    from app.models.stop import Stop


class RouteStop(UUIDPrimaryKeyMixin, Base):
    __tablename__ = "route_stops"

    route_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("routes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    stop_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("stops.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    stop_order: Mapped[int] = mapped_column(Integer, nullable=False)
    estimated_minutes_from_previous: Mapped[int | None] = mapped_column(Integer, nullable=True)

    route: Mapped["Route"] = relationship("Route", back_populates="route_stops")
    stop: Mapped["Stop"] = relationship("Stop")

    __table_args__ = (
        UniqueConstraint("route_id", "stop_order", name="uq_route_stop_order"),
        UniqueConstraint("route_id", "stop_id", name="uq_route_stop_once"),
    )
