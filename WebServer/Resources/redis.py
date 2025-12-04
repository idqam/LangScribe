from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Configure FastAPI Cache on startup"""
    
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    
    redis = aioredis.from_url(
        redis_url,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(
        RedisBackend(redis),
    )
    
    print("FastAPI Cache initialized with Redis backend")
    
    yield

    await redis.close()
    print("Redis connection closed")