from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.chat_models import BaseChatModel

from app.config import settings

_llm: BaseChatModel | None = None


def get_llm() -> BaseChatModel:
    global _llm
    if _llm is None:
        key = (settings.anthropic_api_key or "").strip()
        if not key or len(key) < 40 or "..." in key:
            raise ValueError(
                "ANTHROPIC_API_KEY is missing or incomplete. "
                "Add the full key from console.anthropic.com to ai_agent/.env."
            )
        _llm = ChatAnthropic(
            model=settings.anthropic_model,
            api_key=settings.anthropic_api_key,
            temperature=0.2,
            max_tokens=1024,
        )
    return _llm
