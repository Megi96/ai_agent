from pathlib import Path

from app.rag.loaders import load_document


def test_load_document_returns_placeholder() -> None:
    # Uses a temp-like path; loader returns placeholder content regardless
    docs = load_document(Path("sample.txt"))
    assert len(docs) == 1
    assert "sample.txt" in docs[0].page_content
    assert docs[0].metadata["filename"] == "sample.txt"
