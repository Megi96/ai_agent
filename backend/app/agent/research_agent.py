from app.agent.tools.rag_tool import retrieve_documents
from app.agent.tools.web_search import search_web
from app.models.chat import ChatResponse


class ResearchAgent:
    """Orchestrates RAG retrieval, web search, and Claude synthesis."""

    async def answer(self, question: str, use_web: bool = False) -> ChatResponse:
        doc_sources = await retrieve_documents(question)
        web_sources = await search_web(question) if use_web else []

        all_sources = doc_sources + web_sources

        if not all_sources and not doc_sources:
            return ChatResponse(
                answer=(
                    f'Received your question: "{question}". '
                    "The research agent skeleton is running — full RAG and Claude "
                    "integration coming in Phase 2/3."
                ),
                sources=web_sources,
            )

        source_summary = ", ".join(s.title for s in all_sources) or "no sources yet"
        return ChatResponse(
            answer=(
                f'Placeholder answer for: "{question}". '
                f"Sources found: {source_summary}."
            ),
            sources=all_sources,
        )
