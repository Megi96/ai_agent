from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.document import DocumentMetadata, UploadResponse
from app.rag.ingest import ingest_file
from app.rag.registry import get_document_registry

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)) -> UploadResponse:
    try:
        document = await ingest_file(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return UploadResponse(document=document)


@router.get("", response_model=list[DocumentMetadata])
async def list_documents() -> list[DocumentMetadata]:
    return get_document_registry().list_all()
