from typing import AsyncGenerator

from redis.asyncio import ConnectionPool, Redis

from app.config import settings


class RedisCache:
    def __init__(self):
        pool = ConnectionPool.from_url(settings.REDIS_URL)
        self.redis = Redis(connection_pool=pool)


cache = RedisCache()


async def get_cache() -> AsyncGenerator[Redis, None]:
    async with cache.redis as redis:
        yield redis
