from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Feedback Service")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "feedback-service"}

