from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from langchain_core.documents import Document

from app.config import settings
from app.models.document import DocumentMetadata
from app.rag.chunking import split_documents
from app.rag.loaders import SUPPORTED_EXTENSIONS, load_document
from app.rag.registry import get_document_registry
from app.rag.vectorstore import get_vectorstore


def _validate_extension(filename: str) -> None:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        raise ValueError(f"Unsupported file type '{suffix}'. Supported: {supported}")


def _attach_document_metadata(
    chunks: list[Document],
    *,
    document_id: str,
    filename: str,
    content_type: str,
) -> list[Document]:
    enriched: list[Document] = []
    for index, chunk in enumerate(chunks):
        metadata = {
            **chunk.metadata,
            "document_id": document_id,
            "filename": filename,
            "content_type": content_type,
            "chunk_index": index,
        }
        enriched.append(Document(page_content=chunk.page_content, metadata=metadata))
    return enriched


async def ingest_file(file: UploadFile) -> DocumentMetadata:
    """Load, chunk, embed, and store a document in the vector store."""
    filename = file.filename or "unknown"
    _validate_extension(filename)

    document_id = str(uuid4())
    upload_dir = Path(settings.upload_dir) / document_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / filename
    content = await file.read()
    if not content:
        raise ValueError(f"Uploaded file is empty: {filename}")

    file_path.write_bytes(content)

    raw_documents = load_document(file_path)
    chunks = split_documents(raw_documents)
    if not chunks:
        raise ValueError(f"No content could be chunked from: {filename}")

    enriched_chunks = _attach_document_metadata(
        chunks,
        document_id=document_id,
        filename=filename,
        content_type=file.content_type or "application/octet-stream",
    )

    vectorstore = get_vectorstore()
    vectorstore.add_documents(enriched_chunks)

    metadata = DocumentMetadata(
        id=document_id,
        filename=filename,
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        chunk_count=len(enriched_chunks),
        ingested_at=datetime.now(timezone.utc),
    )
    get_document_registry().add(metadata)
    return metadata
