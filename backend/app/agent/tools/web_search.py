from app.models.chat import Source, SourceType


async def search_web(query: str, max_results: int = 5) -> list[Source]:
    """Search the web for additional context using Tavily or DuckDuckGo."""
    # TODO: implement Tavily / DuckDuckGo integration
    _ = query, max_results
    return [
        Source(
            type=SourceType.WEB,
            title="Placeholder web result",
            snippet="Web search not yet implemented.",
            url="https://example.com",
        )
    ]
