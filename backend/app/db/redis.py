from __future__ import annotations

import json
from typing import Any

import redis.asyncio as redis


class RedisClient:
    def __init__(self, url: str):
        self.client = redis.from_url(url, encoding="utf-8", decode_responses=True)

    async def close(self) -> None:
        await self.client.aclose()

    async def ping(self) -> bool:
        return bool(await self.client.ping())

    async def get_json(self, key: str) -> Any | None:
        raw = await self.client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: Any, expire_seconds: int | None = None) -> None:
        await self.client.set(key, json.dumps(value, default=str), ex=expire_seconds)

    async def delete(self, key: str) -> None:
        await self.client.delete(key)

    async def sadd(self, key: str, *values: str) -> None:
        if values:
            await self.client.sadd(key, *values)

    async def srem(self, key: str, *values: str) -> None:
        if values:
            await self.client.srem(key, *values)

    async def smembers(self, key: str) -> set[str]:
        return set(await self.client.smembers(key))

    async def set_value(self, key: str, value: str, expire_seconds: int | None = None) -> None:
        await self.client.set(key, value, ex=expire_seconds)

    async def get_value(self, key: str) -> str | None:
        return await self.client.get(key)
