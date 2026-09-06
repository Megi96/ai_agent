from fastapi import APIRouter, File, UploadFile

from app.models.document import DocumentMetadata, UploadResponse
from app.rag.ingest import ingest_file

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    document = await ingest_file(file)
    return UploadResponse(document=document)


@router.get("", response_model=list[DocumentMetadata])
async def list_documents() -> list[DocumentMetadata]:
    # TODO: implement listing from vector store metadata
    return []
