# AI Research Agent

**Final scope:** An agent that **searches the web and writes a summary.**

Give it a topic or question → it searches the web (Tavily or DuckDuckGo) → Claude writes a concise, sourced summary. You can optionally upload documents for extra context.

## Architecture

```
User topic → Web Search (Tavily / DuckDuckGo)
                    ↓
         (+ optional user documents via RAG)
                    ↓
              Claude → Summary + source citations
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
- [Anthropic API key](https://console.anthropic.com/) (optional for RAG demo; needed for Claude in Phase 3)

### One-time: create both environments

**Windows (recommended):**

```powershell
.\scripts\setup-all.ps1
```

Or separately:

```powershell
.\scripts\setup-rag-env.ps1   # Python venv → backend/.venv
.\scripts\setup-web-env.ps1   # Node deps  → frontend/node_modules
```

**macOS/Linux:**

```bash
chmod +x scripts/setup-rag-env.sh scripts/setup-web-env.sh
./scripts/setup-rag-env.sh
./scripts/setup-web-env.sh
```

| Environment | Location | Purpose |
|-------------|----------|---------|
| **RAG (Python)** | `backend/.venv/` | FastAPI, LangChain, ChromaDB, embeddings |
| **Web (Node)** | `frontend/node_modules/` | React + Vite demo UI |

### Run the RAG backend

```bash
cd backend

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

uvicorn app.main:app --reload --port 8000
```

### Run the web frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:5173

## Quick demo (first try)

1. Start backend and frontend (two terminals):

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

**Windows shortcut:** `.\scripts\run_demo.ps1` opens both in separate windows.

2. Open http://localhost:5173
3. Click a sample topic or type your own (e.g. *"Summarize trends in AI agents"*)
4. Click **Summarize** — web search runs automatically
5. Optional: upload documents or **Load demo documents** for extra context

Or seed demo docs from the CLI:

```bash
python scripts/seed_demo.py
```

### Optional: ChromaDB via Docker

```bash
docker compose up -d chromadb
```

By default the backend uses a local ChromaDB persist directory at `backend/data/chroma/`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key for Claude answers |
| `ANTHROPIC_MODEL` | No | Claude model (default: `claude-sonnet-4-20250514`) |
| `TAVILY_API_KEY` | No | Tavily API key for web search (falls back to DuckDuckGo) |
| `WEB_SEARCH_MAX_RESULTS` | No | Max web results per query (default: `5`) |
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
| POST | `/demo/seed` | Load bundled demo documents |
| POST | `/chat` | Ask a question (RAG + optional web search) |

## Development Phases

1. **Phase 1:** Folder skeleton + stubs
2. **Phase 2:** RAG ingest + retrieval demo
3. **Phase 3 (current):** Web search + Claude summary (core scope)
4. **Phase 4:** Polish UI, streaming, better citations
5. **Phase 5:** Voice input/output (optional)

## License

MIT
