from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_redis
from app.db.redis import RedisClient

router = APIRouter()


@router.get("")
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: RedisClient = Depends(get_redis),
) -> dict:
    await db.execute(text("SELECT 1"))
    redis_ok = await redis.ping()
    return {
        "status": "ok",
        "database": "ok",
        "redis": "ok" if redis_ok else "error",
    }
