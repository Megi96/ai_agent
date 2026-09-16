from enum import Enum

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    DOCUMENT = "document"
    WEB = "web"


class Source(BaseModel):
    type: SourceType
    title: str
    snippet: str
    url: str | None = None
    document_id: str | None = None


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    use_web: bool = True
    use_documents: bool = True


class ChatResponse(BaseModel):
    answer: str
    sources: list[Source] = Field(default_factory=list)
