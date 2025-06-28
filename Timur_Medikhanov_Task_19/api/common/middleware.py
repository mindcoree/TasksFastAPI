import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import aioredis
from fastapi.responses import JSONResponse

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, redis_url: str, limit: int = 10, window: int = 60):
        super().__init__(app)
        self.redis_url = redis_url
        self.limit = limit
        self.window = window
        self.redis = None

    async def dispatch(self, request: Request, call_next):
        if not self.redis:
            self.redis = await aioredis.from_url(self.redis_url, encoding="utf-8", decode_responses=True)
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}:{int(time.time()) // self.window}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, self.window)
        if count > self.limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        response = await call_next(request)
        return response

