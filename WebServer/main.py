from fastapi import FastAPI

app = FastAPI(title="LangScribe API Gateway")



@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "api-gateway"}
