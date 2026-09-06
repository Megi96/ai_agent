from pathlib import Path

from langchain_core.documents import Document


def load_document(path: str | Path) -> list[Document]:
    """Load a document from disk and return LangChain Document objects."""
    # TODO: implement PDF/DOCX/TXT/Markdown loaders
    path = Path(path)
    return [
        Document(
            page_content=f"Placeholder content for {path.name}",
            metadata={"source": str(path), "filename": path.name},
        )
    ]
