import pytest
from langchain_community.embeddings import FakeEmbeddings

from app.config import settings


@pytest.fixture
def rag_tmp_paths(tmp_path, monkeypatch):
    chroma_dir = tmp_path / "chroma"
    upload_dir = tmp_path / "uploads"
    registry_path = tmp_path / "documents.json"

    monkeypatch.setattr(settings, "chroma_persist_dir", str(chroma_dir))
    monkeypatch.setattr(settings, "upload_dir", str(upload_dir))
    monkeypatch.setattr(settings, "registry_path", str(registry_path))

    import app.rag.embeddings as embeddings_module
    import app.rag.registry as registry_module
    import app.rag.vectorstore as vectorstore_module

    monkeypatch.setattr(
        embeddings_module,
        "_embeddings",
        FakeEmbeddings(size=384),
    )
    vectorstore_module._vectorstore = None
    registry_module._registry = None

    return {
        "chroma_dir": chroma_dir,
        "upload_dir": upload_dir,
        "registry_path": registry_path,
    }
