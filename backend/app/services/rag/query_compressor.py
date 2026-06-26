from __future__ import annotations
from groq import AsyncGroq
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

_COMPRESSION_PROMPT = (
    "Rewrite the following question as a short, keyword-rich search query. "
    "Remove filler words. Preserve all key entities and intent. "
    "Return only the rewritten query, nothing else.\n\nQuestion: {question}"
)


class QueryCompressor:
    def __init__(self) -> None:
        settings = get_settings()
        self._client = AsyncGroq(api_key=settings.groq_api_key)
        self._model = settings.llm_model
        self._enabled = settings.query_compression_enabled

    async def compress(self, question: str) -> tuple[str, bool]:
        if not self._enabled or len(question.split()) <= 8:
            return question, False

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": _COMPRESSION_PROMPT.format(question=question)}],
                max_tokens=64,
                temperature=0.0,
            )
            compressed = response.choices[0].message.content or question
            compressed = compressed.strip().strip('"').strip("'")
            logger.info("query_compressed", original_len=len(question), compressed_len=len(compressed))
            return compressed, True
        except Exception as exc:
            logger.warning("query_compression_failed", error=str(exc))
            return question, False


_instance: QueryCompressor | None = None


def get_query_compressor() -> QueryCompressor:
    global _instance
    if _instance is None:
        _instance = QueryCompressor()
    return _instance