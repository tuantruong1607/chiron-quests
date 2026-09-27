"""Redis connection helper shared across the app and the arq worker."""

from functools import lru_cache

import redis.asyncio as redis

from app.core.config import settings


@lru_cache
def get_redis() -> redis.Redis:
    """Return a process-wide async Redis client built from `settings.REDIS_URL`.

    Cached so callers share one connection pool instead of opening a new
    one per request/job.
    """
    client: redis.Redis = redis.Redis.from_url(settings.REDIS_URL)
    return client
