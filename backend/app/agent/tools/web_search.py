import asyncio
import logging

from app.config import settings
from app.models.chat import Source, SourceType

logger = logging.getLogger(__name__)

PLACEHOLDER_KEYS = {"", "tvly-...", "tvly-", "your-tavily-key"}


def _is_valid_tavily_key(key: str) -> bool:
    cleaned = (key or "").strip()
    if cleaned in PLACEHOLDER_KEYS or "..." in cleaned:
        return False
    return cleaned.startswith("tvly-") and len(cleaned) > 12


def _item_to_source(item: dict) -> Source:
    return Source(
        type=SourceType.WEB,
        title=item.get("title") or "Web result",
        snippet=item.get("content") or item.get("body") or item.get("snippet") or "",
        url=item.get("url") or item.get("href"),
    )


def _search_tavily(query: str, max_results: int) -> list[Source]:
    from tavily import TavilyClient

    client = TavilyClient(api_key=settings.tavily_api_key.strip())
    response = client.search(query=query, max_results=max_results)
    return [_item_to_source(item) for item in response.get("results", [])]


def _search_ddgs(query: str, max_results: int) -> list[Source]:
    """Search the web with the ddgs package (successor to duckduckgo_search)."""
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS

    sources: list[Source] = []
    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=max_results):
            sources.append(_item_to_source(item))
    return sources


async def search_web(query: str, max_results: int | None = None) -> list[Source]:
    """Search the web for every user question — Tavily first, then DuckDuckGo."""
    cleaned_query = query.strip()
    if not cleaned_query:
        return []

    limit = max_results or settings.web_search_max_results

    if _is_valid_tavily_key(settings.tavily_api_key):
        try:
            tavily_results = await asyncio.to_thread(_search_tavily, cleaned_query, limit)
            if tavily_results:
                return tavily_results
            logger.warning("Tavily returned no results for query=%r, falling back to DDG", cleaned_query)
        except Exception as exc:
            logger.warning("Tavily search failed for query=%r: %s — falling back to DDG", cleaned_query, exc)

    try:
        return await asyncio.to_thread(_search_ddgs, cleaned_query, limit)
    except Exception as exc:
        logger.error("Web search failed for query=%r: %s", cleaned_query, exc)
        return []
