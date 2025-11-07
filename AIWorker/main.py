from fastapi import FastAPI

app = FastAPI(title="Feedback Service")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "feedback-service"}
