FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim
WORKDIR /app
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml
RUN python -m spacy download en_core_web_sm
COPY . .
EXPOSE 8002
CMD ["python", "main.py"]
