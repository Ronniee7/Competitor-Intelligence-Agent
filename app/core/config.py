from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    app_name: str = "Competitor Intelligence Agent"

    ollama_url: str = "http://localhost:11434"

    ollama_model: str = "qwen3:4b"

    database_url: str = "sqlite:///./competitor_intelligence.db"

    max_pages_per_competitor: int = 8

    max_page_size: int = 2_000_000

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()