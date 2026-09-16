from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStore
from pathlib import Path

from app.config import settings
from app.rag.embeddings import get_embeddings

_vectorstore: VectorStore | None = None


def get_vectorstore() -> VectorStore:
    global _vectorstore
    if _vectorstore is None:
        Path(settings.chroma_persist_dir).mkdir(parents=True, exist_ok=True)
        _vectorstore = Chroma(
            collection_name="research_agent",
            persist_directory=settings.chroma_persist_dir,
            embedding_function=get_embeddings(),
        )
    return _vectorstore
