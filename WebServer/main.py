from fastapi import FastAPI
import uvicorn

app = FastAPI(title="LangScribe API Gateway")

@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


