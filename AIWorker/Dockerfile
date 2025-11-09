FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY uv.lock ./ 
COPY AIWorker/ ./ 

RUN uv sync --frozen --no-dev 

EXPOSE 8001

CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
