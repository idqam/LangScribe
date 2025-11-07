# LangScribe

Writing-first language learning platform.

## Architecture

- **Web-Server** (8000) - Routes & auth
- **AI-Worker** (8001) - Daily prompts and AI feedback processing
- **Progress Analytics Service** - Tracks user progress and analytics

## Development

### Backend
```bash
cd WebServer
uv sync
uv run uvicorn main:app --host 0.0.0.0 --port 8000
```

## Tech Stack

**Backend:** Python 3.11 + FastAPI + UV  
**Data:** Supabase + Cosmos DB + Redis  
**AI:** OpenAI + Anthropic  
**Infra:** Docker + AWS
