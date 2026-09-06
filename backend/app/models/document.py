from datetime import datetime

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    id: str
    filename: str
    content_type: str
    size_bytes: int
    chunk_count: int = 0
    ingested_at: datetime


class UploadResponse(BaseModel):
    document: DocumentMetadata
    message: str = "Document uploaded successfully"
