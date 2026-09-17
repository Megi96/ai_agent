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

- **Backend:** Python, FastAPI, LangChain, ChromaDB, HuggingFace embeddings, Anthropic Claude
- **Frontend:** React, Vite, TypeScript
- **Web search:** Tavily (optional) or DuckDuckGo via `ddgs`

## Project Structure

```
ai_agent/
├── backend/          # FastAPI API, RAG pipeline, research agent
├── frontend/         # React demo UI
├── scripts/          # Dev helpers, setup, and demo seeding
└── .env              # API keys and config (project root — not committed)
```

---

## Progress

### Done so far

#### Phase 1 — Project skeleton
- FastAPI app with health, chat, and document routes
- React + Vite frontend scaffold
- Docker Compose stub for ChromaDB
- Git hooks to strip Cursor co-author lines from commits

#### Phase 2 — RAG (document ingest + retrieval)
- Document loaders for **PDF, DOCX, TXT, Markdown**
- Text chunking with configurable size/overlap
- HuggingFace embeddings (`all-MiniLM-L6-v2`) + ChromaDB vector store
- Document upload API and metadata registry
- Semantic retrieval wired into the research agent
- Demo documents and `POST /demo/seed` endpoint
- Backend tests for ingest and retrieval

#### Phase 3 — Web search + Claude summaries (core scope)
- Web search via **Tavily** when a valid key is set; falls back to **DuckDuckGo** (`ddgs`) for free search
- Placeholder API keys (e.g. `tvly-...`) are rejected so DuckDuckGo is used instead
- Claude synthesis through LangChain (`ChatAnthropic`)
- Prose-style summaries (no numbered lists); sources shown separately in the UI
- Config loads `.env` from the **project root** (`ai_agent/.env`)
- Friendly error messages for missing/invalid API keys and model errors
- Default model: `claude-sonnet-4-6` (Sonnet 4 was retired mid-2026)
- Tests for web search and agent flow (mocked LLM/search)

#### Phase 4 — UI polish (partial)
- Minimal **white + light blue** theme
- Document upload panel with file list and demo seed button
- Chat panel with sample topics, “Include my documents” toggle, and source chips (Web / Doc)
- Formatted answer rendering (paragraph layout, no stray numbering)
- Larger chat window (sidebar capped, chat fills remaining space)
- API online/offline status indicator
- Setup scripts: `setup-all.ps1`, `setup-rag-env`, `setup-web-env`, `run_demo.ps1`

#### Repository
- Initial scaffold and full feature work pushed to GitHub (`origin/master`)

---

### What's next

#### Phase 4 — Remaining UI / UX
- [ ] **Streaming responses** — show the summary as Claude generates it
- [ ] **Better citations** — clearer link between answer text and source chips
- [ ] **Document management** — delete documents, dedupe on repeated demo seed
- [ ] **Mobile layout** — refine stacked layout on small screens

#### Phase 5 — Voice (optional)
- [ ] Speech-to-text input (`backend/app/voice/` stub exists)
- [ ] Text-to-speech for summaries

#### Backend hardening
- [ ] Rate limiting and upload size caps
- [ ] More integration tests with real API mocks
- [ ] Optional: rename default branch `master` → `main`

---

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- [Anthropic API key](https://console.anthropic.com/) — **required** for summaries

Copy `.env.example` to `.env` at the project root and set your keys:

```bash
cp .env.example .env   # macOS/Linux
# edit .env — paste full ANTHROPIC_API_KEY (not sk-ant-...)
```

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

### Run the backend

```bash
cd backend

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

uvicorn app.main:app --reload --port 8000
```

### Run the frontend

```bash
cd frontend
npm run dev
```

Open http://localhost:5173

> **Important:** Restart the backend after any change to `.env`.

---

## Quick demo (first try)

1. Start backend and frontend (two terminals), or on Windows run `.\scripts\run_demo.ps1`
2. Open http://localhost:5173
3. Click a sample topic or type your own (e.g. *"Summarize trends in AI agents"*)
4. Click **Summarize** — web search runs automatically
5. Optional: upload documents or click **Load demo documents** for extra context

Seed demo docs from the CLI:

```bash
python scripts/seed_demo.py
```

### Optional: ChromaDB via Docker

```bash
docker compose up -d chromadb
```

By default the backend uses a local ChromaDB persist directory at `backend/data/chroma/` (when run from `backend/`).

---

## Environment Variables

All variables go in `ai_agent/.env` at the project root.

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Full Anthropic API key for Claude summaries |
| `ANTHROPIC_MODEL` | No | Claude model (default: `claude-sonnet-4-6`) |
| `TAVILY_API_KEY` | No | Tavily API key for web search (falls back to DuckDuckGo if empty) |
| `WEB_SEARCH_MAX_RESULTS` | No | Max web results per query (default: `5`) |
| `CHROMA_PERSIST_DIR` | No | Vector DB storage path (default: `./data/chroma`) |
| `UPLOAD_DIR` | No | Uploaded file storage (default: `./data/uploads`) |
| `REGISTRY_PATH` | No | Document metadata JSON (default: `./data/documents.json`) |
| `EMBEDDING_MODEL` | No | HuggingFace model (default: `all-MiniLM-L6-v2`) |
| `CHUNK_SIZE` / `CHUNK_OVERLAP` | No | RAG chunking (default: `1000` / `200`) |
| `RETRIEVAL_TOP_K` | No | Document chunks retrieved per query (default: `5`) |
| `BACKEND_PORT` | No | API port (default: `8000`) |
| `FRONTEND_PORT` | No | Frontend dev port (default: `5173`) |

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/documents/upload` | Upload a document for ingestion |
| GET | `/documents` | List ingested documents |
| POST | `/demo/seed` | Load bundled demo documents |
| POST | `/chat` | Ask a question (web search + optional RAG + Claude summary) |

### Chat request body

```json
{
  "question": "Summarize trends in AI agents",
  "use_web": true,
  "use_documents": true
}
```

---

## Tests

From `backend/` with the venv activated:

```bash
python -m pytest tests/ -q
```

Covers document ingest, web search (mocked), and agent flow (mocked LLM).

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| “needs ANTHROPIC_API_KEY in .env” | Key missing, truncated, or placeholder (`sk-ant-...`) | Paste the **full** key from console.anthropic.com |
| Model 404 error | Old model name in `.env` | Set `ANTHROPIC_MODEL=claude-sonnet-4-6` and restart backend |
| No web results | Missing `ddgs` or bad Tavily placeholder | `pip install ddgs` or remove placeholder `TAVILY_API_KEY` |
| Documents not in summary | Generic question or checkbox off | Check **Include my documents**; ask about your file content |
| UI changes not visible | Stale dev server | Hard refresh (`Ctrl+Shift+R`) or restart `npm run dev` |

---

## License

MIT
