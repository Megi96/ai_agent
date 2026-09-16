import json
from pathlib import Path

from app.config import settings
from app.models.document import DocumentMetadata


class DocumentRegistry:
    """Persist document metadata for listing and retrieval attribution."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path(settings.registry_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[DocumentMetadata]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [DocumentMetadata.model_validate(item) for item in raw]

    def _write(self, documents: list[DocumentMetadata]) -> None:
        payload = [doc.model_dump(mode="json") for doc in documents]
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add(self, document: DocumentMetadata) -> None:
        documents = self._read()
        documents.append(document)
        self._write(documents)

    def list_all(self) -> list[DocumentMetadata]:
        return sorted(self._read(), key=lambda doc: doc.ingested_at, reverse=True)

    def get(self, document_id: str) -> DocumentMetadata | None:
        for document in self._read():
            if document.id == document_id:
                return document
        return None


_registry: DocumentRegistry | None = None


def get_document_registry() -> DocumentRegistry:
    global _registry
    if _registry is None:
        _registry = DocumentRegistry()
    return _registry
