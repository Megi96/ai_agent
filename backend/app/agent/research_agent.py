import logging

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.llm import get_llm
from app.agent.prompts import (
    MISSING_API_KEY_MESSAGE,
    NO_CONTEXT_MESSAGE,
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
)
from app.agent.tools.rag_tool import retrieve_documents
from app.agent.tools.web_search import search_web
from app.models.chat import ChatResponse, Source

logger = logging.getLogger(__name__)


def _format_source_block(sources: list[Source], label: str) -> str:
    if not sources:
        return f"{label}: (none)"

    lines = [f"{label}:"]
    for source in sources:
        lines.append(f"• {source.title}\n{source.snippet}")
    return "\n\n".join(lines)


def _fallback_summary(question: str, doc_sources: list[Source], web_sources: list[Source]) -> str:
    parts = [f'Research topic: "{question}".', MISSING_API_KEY_MESSAGE]
    if web_sources:
        parts.append("Web results:\n" + _format_source_block(web_sources[:5], "Web"))
    if doc_sources:
        parts.append("Your documents:\n" + _format_source_block(doc_sources[:3], "Documents"))
    return "\n\n".join(parts)


class ResearchAgent:
    """Searches the web (and optional user documents), then writes a summary."""

    async def answer(
        self,
        question: str,
        use_web: bool = True,
        use_documents: bool = True,
    ) -> ChatResponse:
        # Every question is searched on the web — `question` is whatever the user typed.
        logger.info("Processing question: %r (web=%s, docs=%s)", question, use_web, use_documents)
        web_sources = await search_web(question) if use_web else []
        doc_sources = await retrieve_documents(question) if use_documents else []
        all_sources = web_sources + doc_sources

        if not all_sources:
            if use_web and not web_sources:
                return ChatResponse(
                    answer=(
                        f'Could not find web results for: "{question}". '
                        "Restart the backend after running: pip install ddgs. "
                        "Or set a real TAVILY_API_KEY in .env (remove placeholder tvly-...)."
                    ),
                    sources=[],
                )
            return ChatResponse(answer=NO_CONTEXT_MESSAGE, sources=[])

        try:
            answer = await self._write_summary(question, doc_sources, web_sources)
        except ValueError:
            answer = _fallback_summary(question, doc_sources, web_sources)
        except Exception as exc:
            logger.exception("Summary generation failed for question=%r", question)
            error_text = str(exc).lower()
            if "authentication" in error_text or "401" in error_text or "api key" in error_text:
                answer = (
                    "Your Anthropic API key is invalid or missing. "
                    "Open ai_agent/.env and set a full ANTHROPIC_API_KEY from "
                    "https://console.anthropic.com/ — then restart the backend."
                )
            else:
                answer = (
                    f"Summary generation failed: {exc}. "
                    "Web sources are listed below — check backend logs for details."
                )

        return ChatResponse(answer=answer, sources=all_sources)

    async def _write_summary(
        self,
        question: str,
        doc_sources: list[Source],
        web_sources: list[Source],
    ) -> str:
        llm = get_llm()
        user_prompt = USER_PROMPT_TEMPLATE.format(
            question=question,
            web_results=_format_source_block(web_sources, "Web"),
            document_context=_format_source_block(doc_sources, "Documents"),
        )
        response = await llm.ainvoke(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=user_prompt),
            ]
        )
        content = response.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            text_parts = [block.get("text", "") for block in content if isinstance(block, dict)]
            return "\n".join(text_parts).strip()
        return str(content).strip()
