FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
WORKDIR /app
COPY pyproject.toml ./
COPY uv.lock ./ 
RUN uv sync --frozen --no-dev 
COPY AIWorker/ ./ 
EXPOSE 8001
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
