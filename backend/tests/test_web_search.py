import pytest

from app.agent.tools import web_search as web_search_module
from app.models.chat import Source, SourceType


def test_valid_tavily_key_rejects_placeholders() -> None:
    assert web_search_module._is_valid_tavily_key("") is False
    assert web_search_module._is_valid_tavily_key("tvly-...") is False
    assert web_search_module._is_valid_tavily_key("tvly-abc123realkey") is True


def test_search_ddgs_helper(monkeypatch) -> None:
    def fake_ddgs(query: str, max_results: int) -> list[Source]:
        assert query == "any user question"
        _ = max_results
        return [
            Source(
                type=SourceType.WEB,
                title="Example",
                snippet="Example snippet.",
                url="https://example.com",
            )
        ]

    monkeypatch.setattr(web_search_module, "_search_ddgs", fake_ddgs)
    results = web_search_module._search_ddgs("any user question", 3)
    assert len(results) == 1


@pytest.mark.asyncio
async def test_search_web_falls_back_to_ddgs_for_invalid_tavily(monkeypatch) -> None:
    def fake_ddgs(query: str, max_results: int) -> list[Source]:
        assert query == "meaning of medicine"
        _ = max_results
        return [
            Source(
                type=SourceType.WEB,
                title="Medicine definition",
                snippet="Medicine is the science of healing.",
                url="https://example.com/medicine",
            )
        ]

    monkeypatch.setattr(web_search_module.settings, "tavily_api_key", "tvly-...")
    monkeypatch.setattr(web_search_module, "_search_ddgs", fake_ddgs)

    async def fake_to_thread(func, query, limit):
        return func(query, limit)

    monkeypatch.setattr(web_search_module.asyncio, "to_thread", fake_to_thread)

    sources = await web_search_module.search_web("meaning of medicine")
    assert len(sources) == 1
    assert "Medicine" in sources[0].snippet


@pytest.mark.asyncio
async def test_search_web_uses_any_question_not_hardcoded(monkeypatch) -> None:
    captured: list[str] = []

    def fake_ddgs(query: str, max_results: int) -> list[Source]:
        captured.append(query)
        _ = max_results
        return [
            Source(
                type=SourceType.WEB,
                title="Result",
                snippet=f"Answer about {query}",
                url="https://example.com",
            )
        ]

    monkeypatch.setattr(web_search_module.settings, "tavily_api_key", "")
    monkeypatch.setattr(web_search_module, "_search_ddgs", fake_ddgs)

    async def fake_to_thread(func, query, limit):
        return func(query, limit)

    monkeypatch.setattr(web_search_module.asyncio, "to_thread", fake_to_thread)

    await web_search_module.search_web("quantum computing trends")
    await web_search_module.search_web("what is RAG")

    assert captured == ["quantum computing trends", "what is RAG"]
