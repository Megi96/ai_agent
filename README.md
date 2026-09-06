# AI Research Agent

A research assistant that ingests your documents into a RAG pipeline, answers questions about them, and optionally searches the web for additional context.

## Architecture

```
Documents → Ingest → ChromaDB (vector store)
                          ↓
User question → Research Agent → Claude (Anthropic)
                     ↓              ↓
              Web Search      Synthesized answer + citations
```

## Stack

- **Backend:** Python, FastAPI, LangChain, ChromaDB, Anthropic Claude
- **Frontend:** React, Vite, TypeScript
- **Web search:** Tavily (optional) or DuckDuckGo

## Project Structure

```
ai_agent/
├── backend/          # FastAPI API, RAG pipeline, research agent
├── frontend/         # React demo UI
└── scripts/          # Dev helpers and demo seeding
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Anthropic API key](https://console.anthropic.com/)

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
cp ../.env.example ../.env
# Edit .env and add your ANTHROPIC_API_KEY

uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

### Optional: ChromaDB via Docker

```bash
docker compose up -d chromadb
```

By default the backend uses a local ChromaDB persist directory at `backend/data/chroma/`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude |
| `TAVILY_API_KEY` | No | Tavily API key for web search |
| `CHROMA_PERSIST_DIR` | No | Vector DB storage path (default: `./backend/data/chroma`) |
| `UPLOAD_DIR` | No | Uploaded file storage (default: `./backend/data/uploads`) |
| `BACKEND_PORT` | No | API port (default: `8000`) |
| `FRONTEND_PORT` | No | Frontend dev port (default: `5173`) |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/documents/upload` | Upload a document for ingestion |
| GET | `/documents` | List ingested documents |
| POST | `/chat` | Ask a question (RAG + optional web search) |

## Development Phases

1. **Phase 1 (current):** Folder skeleton + stubs
2. **Phase 2:** RAG ingest pipeline (PDF/DOCX/TXT → ChromaDB)
3. **Phase 3:** Research agent (Claude + RAG + web search)
4. **Phase 4:** Live frontend wiring + source citations UI
5. **Phase 5:** Voice module (STT/TTS)

## License

MIT
