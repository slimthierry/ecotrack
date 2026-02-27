from redis.asyncio import Redis, from_url

from app.config.settings import settings

_redis_client: Redis | None = None


async def get_redis() -> Redis:
    """Get or create a Redis connection."""
    global _redis_client
    if _redis_client is None:
        _redis_client = from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_client


async def close_redis() -> None:
    """Close the Redis connection."""
    global _redis_client
    if _redis_client is not None:
        await _redis_client.close()
        _redis_client = None
