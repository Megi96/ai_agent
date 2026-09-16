from io import BytesIO

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.datastructures import UploadFile

from app.agent.research_agent import ResearchAgent
from app.main import app
from app.models.chat import Source, SourceType
from app.rag.ingest import ingest_file
from app.rag.registry import get_document_registry
from app.agent.tools.rag_tool import retrieve_documents


@pytest.mark.asyncio
async def test_health_check() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_chat_without_documents(rag_tmp_paths) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/chat", json={"question": "Hello?", "use_web": False})
    assert response.status_code == 200
    data = response.json()
    assert "No web or document sources" in data["answer"]
    assert data["sources"] == []


@pytest.mark.asyncio
async def test_ingest_and_retrieve_document(rag_tmp_paths) -> None:
    content = (
        "Retrieval-augmented generation combines search with language models. "
        "ChromaDB stores vector embeddings for semantic lookup."
    )
    upload = UploadFile(
        filename="rag-notes.txt",
        file=BytesIO(content.encode("utf-8")),
        headers={"content-type": "text/plain"},
    )

    metadata = await ingest_file(upload)

    assert metadata.filename == "rag-notes.txt"
    assert metadata.chunk_count >= 1

    registry = get_document_registry().list_all()
    assert len(registry) == 1
    assert registry[0].id == metadata.id

    sources = await retrieve_documents("vector embeddings semantic lookup")
    assert len(sources) >= 1
    assert any("ChromaDB" in source.snippet or "vector" in source.snippet.lower() for source in sources)


@pytest.mark.asyncio
async def test_seed_demo_endpoint(rag_tmp_paths, monkeypatch) -> None:
    from app.api.routes import demo as demo_route

    demo_dir = rag_tmp_paths["upload_dir"].parent / "demo"
    demo_dir.mkdir()
    (demo_dir / "sample.txt").write_text("Demo content about vector search.", encoding="utf-8")
    monkeypatch.setattr(demo_route, "DEMO_DIR", demo_dir)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/demo/seed")

    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert len(payload["documents"]) == 1


@pytest.mark.asyncio
async def test_chat_synthesis_with_mock(rag_tmp_paths, monkeypatch) -> None:
    upload = UploadFile(
        filename="stack.txt",
        file=BytesIO(b"The stack uses FastAPI, React, and ChromaDB for RAG."),
        headers={"content-type": "text/plain"},
    )
    await ingest_file(upload)

    async def fake_write_summary(
        self,
        question: str,
        doc_sources: list[Source],
        web_sources: list[Source],
    ) -> str:
        _ = question, doc_sources, web_sources
        return "The project uses FastAPI, React, and ChromaDB."

    monkeypatch.setattr(ResearchAgent, "_write_summary", fake_write_summary)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            json={"question": "What is the technical stack?", "use_web": False},
        )

    assert response.status_code == 200
    data = response.json()
    assert "FastAPI" in data["answer"]
    assert len(data["sources"]) >= 1


@pytest.mark.asyncio
async def test_chat_with_web_search_mock(rag_tmp_paths, monkeypatch) -> None:
    async def fake_web(query: str, max_results: int | None = None) -> list[Source]:
        _ = query, max_results
        return [
            Source(
                type=SourceType.WEB,
                title="Web article",
                snippet="Latest news about retrieval-augmented generation.",
                url="https://example.com/rag",
            )
        ]

    async def fake_write_summary(
        self,
        question: str,
        doc_sources: list[Source],
        web_sources: list[Source],
    ) -> str:
        _ = question, doc_sources
        return f"Summary using {len(web_sources)} web source(s)."

    monkeypatch.setattr("app.agent.research_agent.search_web", fake_web)
    monkeypatch.setattr(ResearchAgent, "_write_summary", fake_write_summary)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/chat",
            json={"question": "What is RAG?", "use_web": True},
        )

    assert response.status_code == 200
    data = response.json()
    assert "web source" in data["answer"].lower()
    assert any(source["type"] == "web" for source in data["sources"])


@pytest.mark.asyncio
async def test_upload_endpoint(rag_tmp_paths) -> None:
    transport = ASGITransport(app=app)
    files = {"file": ("demo.txt", b"FastAPI serves the research agent API.", "text/plain")}

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/documents/upload", files=files)

        assert response.status_code == 200
        payload = response.json()
        assert payload["document"]["filename"] == "demo.txt"
        assert payload["document"]["chunk_count"] >= 1

        list_response = await client.get("/documents")
        assert list_response.status_code == 200
        documents = list_response.json()
        assert len(documents) == 1
