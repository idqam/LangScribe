import os

from fastapi import FastAPI
from Routers import (
    admin_users_router,
    auth_router,
    language_router,
    prompt_router,
    report_router,
    subscription_router,
    user_languages_router,
    user_message_router,
    users_router,
    # jobs_router
)
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
import redis.asyncio as redis
from Resources import OpenAIClient
from contextlib import asynccontextmanager
# from fastapi_cache.decorator import cache

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = redis.from_url("redis://redis:6379")
    FastAPICache.init(RedisBackend(redis_client), prefix="cache")
    client = OpenAIClient()
    yield

app = FastAPI(title="LangScribe API Gateway", lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "https://google.com",
    "http://ai-worker:8001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    max_age=3600,
    same_site="lax",
    https_only=False, ## change on prod
)

routers = [
    auth_router,
    admin_users_router,
    users_router,
    user_message_router,
    user_languages_router,
    report_router,
    prompt_router,
    language_router,
    subscription_router,
    # jobs_router
]

for router in routers:
    app.include_router(router)

@app.post("/health")
async def health() -> dict[str, str]:
    return {"status": "cool", "service": "vibing"}


