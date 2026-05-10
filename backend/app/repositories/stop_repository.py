from __future__ import annotations

from app.models.stop import Stop
from app.repositories.base import BaseRepository


class StopRepository(BaseRepository[Stop]):
    model = Stop
