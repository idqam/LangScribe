# LangScribe

Writing-first language learning platform.

## Architecture

- **Web-Server** (8000) - Routes & auth
- **AI-Worker** (8001) - Daily prompts - Progress tracking Analytics Service
- **Web** (3000) - Next.js
- **Mobile** - React Native (Expo)

## Development

### Backend
```bash
cd services/WebServer
uv pip install -r pyproject.toml
uv run uvicorn main:app
```

## Tech Stack

**Backend:** Python 3.11 + FastAPI + UV  
**Data:** Supabase + Cosmos DB + Redis  
**AI:** OpenAI + Anthropic  
**Infra:** Docker + AWS
