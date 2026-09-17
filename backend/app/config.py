from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root is ai_agent/ (two levels above backend/app/)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]

# Load root .env first (where users put keys), then backend/.env if present
_env_candidates = [PROJECT_ROOT / ".env", BACKEND_ROOT / ".env"]
ENV_FILES = tuple(str(path) for path in _env_candidates if path.exists()) or (".env",)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"
    tavily_api_key: str = ""
    web_search_max_results: int = 5
    chroma_persist_dir: str = "./data/chroma"
    upload_dir: str = "./data/uploads"
    registry_path: str = "./data/documents.json"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    retrieval_top_k: int = 5
    backend_port: int = 8000
    frontend_port: int = 5173


settings = Settings()
