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
)
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="LangScribe API Gateway")

origins = [
    "http://localhost:3000",
    "https://google.com",
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
]

for router in routers:
    app.include_router(router)


@app.post("/health")
async def health() -> dict[str, str]:
    return {"status": "cool", "service": "vibing"}
