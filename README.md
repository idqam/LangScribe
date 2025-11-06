# LangScribe

Writing-first language learning platform.

## Architecture

- **API Gateway** (8080) - Routes & auth
- **Prompt Engine** (8001) - Daily prompts
- **Feedback Service** (8002) - AI feedback
- **Analytics Service** (8003) - Progress tracking
- **SRS Service** (8004) - Spaced repetition
- **Web** (3000) - Next.js
- **Mobile** - React Native (Expo)

## Quick Start

```bash
cd LangScribe
cp .env.example .env
docker-compose up --build
```

Visit http://localhost:3000

## Development

### Backend
```bash
cd services/[service-name]
uv pip install -r pyproject.toml
python main.py
```

### Web
```bash
cd frontend/web
npm install
npm run dev
```

### Mobile
```bash
cd frontend/mobile
npm install
npx expo start
```

## Tech Stack

**Backend:** Python 3.11 + FastAPI + UV  
**Frontend:** Next.js 14 + React Native (Expo)  
**Data:** Supabase + Cosmos DB + Redis  
**AI:** OpenAI + Anthropic  
**Infra:** Docker + AWS ECS
