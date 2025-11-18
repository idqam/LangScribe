from fastapi import FastAPI
from Routers import (
    language_router,
    prompt_router,
    report_router,
    subscription_router,
    user_languages_router,
    user_message_router,
    user_router,
)

app = FastAPI(title="LangScribe API Gateway")


routers = [
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
