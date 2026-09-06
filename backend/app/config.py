from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    anthropic_api_key: str = ""
    tavily_api_key: str = ""
    chroma_persist_dir: str = "./backend/data/chroma"
    upload_dir: str = "./backend/data/uploads"
    backend_port: int = 8000
    frontend_port: int = 5173


settings = Settings()
