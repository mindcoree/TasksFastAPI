from typing import Any, AsyncGenerator

import redis.asyncio as redis
from fastapi import FastAPI
from redis.asyncio import Redis

from core.config import settings

redis_client = None


async def get_redis(app: FastAPI) -> AsyncGenerator[Redis[Any] | None, Any]:
    global redis_client
    redis_client = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    app.state.redis = redis_client
    try:
        await redis_client.ping()
        yield redis_client
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")
        yield None
    finally:
        await redis_client.close()


async def shutdown_redis(app: FastAPI) -> None:
    if app.state.redis:
        await app.state.redis.close()
        print("Successfully closed Redis")
