from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Server
    port: int = 8000
    environment: str = "development"

    # Groq
    groq_api_key: str

    # Models
    embedding_model: str = "nomic-embed-text"
    llm_model: str = "llama3-8b-8192"

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 64

    # Retrieval
    max_retrieved_chunks: int = 4
    max_context_tokens: int = 3000

    # Semantic cache
    semantic_cache_ttl_seconds: int = 3600
    semantic_cache_similarity_threshold: float = 0.92

    # Query compression
    query_compression_enabled: bool = True

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
