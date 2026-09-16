from pathlib import Path

import pytest

from app.rag.chunking import split_documents
from app.rag.loaders import load_document


def test_load_txt_document(tmp_path: Path) -> None:
    file_path = tmp_path / "notes.txt"
    file_path.write_text("Research notes about vector databases.", encoding="utf-8")

    docs = load_document(file_path)

    assert len(docs) == 1
    assert "vector databases" in docs[0].page_content
    assert docs[0].metadata["filename"] == "notes.txt"


def test_load_markdown_document(tmp_path: Path) -> None:
    file_path = tmp_path / "readme.md"
    file_path.write_text("# Title\n\nMarkdown body.", encoding="utf-8")

    docs = load_document(file_path)

    assert len(docs) == 1
    assert "Markdown body" in docs[0].page_content


def test_split_documents_creates_chunks() -> None:
    from langchain_core.documents import Document

    long_text = "word " * 500
    docs = [Document(page_content=long_text, metadata={"filename": "long.txt"})]

    chunks = split_documents(docs)

    assert len(chunks) > 1
    assert all(chunk.metadata["filename"] == "long.txt" for chunk in chunks)


def test_unsupported_extension_raises(tmp_path: Path) -> None:
    file_path = tmp_path / "image.png"
    file_path.write_bytes(b"fake")

    with pytest.raises(ValueError, match="Unsupported file type"):
        load_document(file_path)
