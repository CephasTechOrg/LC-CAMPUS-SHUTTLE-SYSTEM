from __future__ import annotations

from app.models.shuttle import Shuttle
from app.repositories.base import BaseRepository


class ShuttleRepository(BaseRepository[Shuttle]):
    model = Shuttle
