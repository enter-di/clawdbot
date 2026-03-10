"""Redis-backed sliding window rate limiter."""

import time

import redis.asyncio as aioredis

from openclaw.config import settings


class RateLimiter:
    def __init__(self, redis_client: aioredis.Redis) -> None:
        self._redis = redis_client
        self._limit = settings.rate_limit_requests
        self._window = settings.rate_limit_window_seconds

    async def is_allowed(self, chat_id: int) -> bool:
        """Return True if the request is within the rate limit."""
        now = int(time.time())
        bucket = now // self._window
        key = f"ratelimit:{chat_id}:{bucket}"

        count = await self._redis.incr(key)
        if count == 1:
            await self._redis.expire(key, self._window * 2)

        return count <= self._limit
