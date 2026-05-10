from __future__ import annotations

from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, entity_id: UUID) -> ModelT | None:
        return await self.db.get(self.model, entity_id)

    async def list(self, limit: int = 100, offset: int = 0) -> list[ModelT]:
        result = await self.db.execute(select(self.model).limit(limit).offset(offset))
        return list(result.scalars().all())

    async def add(self, entity: ModelT) -> ModelT:
        self.db.add(entity)
        await self.db.flush()
        await self.db.refresh(entity)
        return entity

    async def commit(self) -> None:
        await self.db.commit()

    async def refresh(self, entity: ModelT) -> None:
        await self.db.refresh(entity)

    def apply_updates(self, entity: ModelT, values: dict[str, Any]) -> ModelT:
        for key, value in values.items():
            if value is not None:
                setattr(entity, key, value)
        return entity
