from io import BytesIO
from pathlib import Path

from fastapi import APIRouter, HTTPException
from starlette.datastructures import UploadFile

from app.models.document import DocumentMetadata
from app.rag.ingest import ingest_file
from app.rag.loaders import SUPPORTED_EXTENSIONS

router = APIRouter(prefix="/demo", tags=["demo"])

DEMO_DIR = Path(__file__).resolve().parents[3] / "data" / "demo"


@router.post("/seed")
async def seed_demo_documents() -> dict[str, list[DocumentMetadata] | int | str]:
    """Ingest bundled demo documents for a quick first try."""
    if not DEMO_DIR.exists():
        raise HTTPException(status_code=404, detail=f"Demo directory not found: {DEMO_DIR}")

    files = sorted(
        path
        for path in DEMO_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    if not files:
        raise HTTPException(status_code=404, detail="No demo files available")

    ingested: list[DocumentMetadata] = []
    for path in files:
        content = path.read_bytes()
        upload = UploadFile(
            filename=path.name,
            file=BytesIO(content),
            headers={"content-type": "application/octet-stream"},
        )
        ingested.append(await ingest_file(upload))

    return {
        "message": f"Ingested {len(ingested)} demo document(s)",
        "count": len(ingested),
        "documents": ingested,
    }
