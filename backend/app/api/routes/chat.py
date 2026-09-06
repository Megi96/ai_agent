from fastapi import APIRouter

from app.agent.research_agent import ResearchAgent
from app.models.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["chat"])

_agent = ResearchAgent()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    return await _agent.answer(question=request.question, use_web=request.use_web)
