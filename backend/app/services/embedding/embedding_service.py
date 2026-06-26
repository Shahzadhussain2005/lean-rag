from __future__ import annotations
from app.core.logging import get_logger

logger = get_logger(__name__)

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("loading_embedding_model", model="all-MiniLM-L6-v2")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        logger.info("embedding_model_loaded")
    return _model


class EmbeddingService:
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = _get_model()
        embeddings = model.encode(texts, show_progress_bar=False)
        return [e.tolist() for e in embeddings]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]


_instance: EmbeddingService | None = None


def get_embedding_service() -> EmbeddingService:
    global _instance
    if _instance is None:
        _instance = EmbeddingService()
    return _instance