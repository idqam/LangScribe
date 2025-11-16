from fastapi import FastAPI

app = FastAPI(title="LangScribe API Gateway")


@app.post("/health")
async def health() -> dict[str, str]:
    return {"status": "cool", "service": "vibing"}
