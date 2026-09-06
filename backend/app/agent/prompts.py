SYSTEM_PROMPT = """You are a research assistant. Answer questions using the provided document context
and web search results when available. Always cite your sources."""

USER_PROMPT_TEMPLATE = """Question: {question}

Document context:
{document_context}

Web search results:
{web_results}

Provide a clear, well-sourced answer."""
