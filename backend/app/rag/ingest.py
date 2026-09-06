from datetime import datetime, timezone
from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.models.document import DocumentMetadata
from app.rag.loaders import load_document
from app.rag.vectorstore import get_vectorstore


async def ingest_file(file: UploadFile) -> DocumentMetadata:
    """Load, chunk, embed, and store a document in the vector store."""
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename
    content = await file.read()
    file_path.write_bytes(content)

    documents = load_document(file_path)
    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents)

    return DocumentMetadata(
        id=file_path.stem,
        filename=file.filename or "unknown",
        content_type=file.content_type or "application/octet-stream",
        size_bytes=len(content),
        chunk_count=len(documents),
        ingested_at=datetime.now(timezone.utc),
    )
