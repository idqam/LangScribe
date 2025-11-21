import os

from fastapi import FastAPI
from Routers import (
    auth_router,
    language_router,
    prompt_router,
    report_router,
    subscription_router,
    user_languages_router,
    user_message_router,
    user_router,
)
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(title="LangScribe API Gateway")

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY"),
    max_age=3600,
    same_site="lax",
    https_only=False,
)

routers = [
    auth_router,
    user_router,
    user_message_router,
    user_languages_router,
    report_router,
    prompt_router,
    language_router,
    subscription_router,
]

for router in routers:
    app.include_router(router)


@app.post("/health")
async def health() -> dict[str, str]:
    return {"status": "cool", "service": "vibing"}
