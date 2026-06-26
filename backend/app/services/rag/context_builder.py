from __future__ import annotations
from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.domain import RetrievedChunk

logger = get_logger(__name__)


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


class ContextBuilder:
    def __init__(self) -> None:
        settings = get_settings()
        self._max_tokens = settings.max_context_tokens

    def build(self, chunks: list[RetrievedChunk]) -> tuple[str, list[RetrievedChunk]]:
        selected: list[RetrievedChunk] = []
        used_tokens = 0

        for rc in chunks:
            chunk_tokens = rc.chunk.token_count or _estimate_tokens(rc.chunk.text)
            if used_tokens + chunk_tokens > self._max_tokens:
                break
            selected.append(rc)
            used_tokens += chunk_tokens

        context_parts = [
            f"[Source {i + 1}]\n{rc.chunk.text}"
            for i, rc in enumerate(selected)
        ]
        context = "\n\n---\n\n".join(context_parts)

        logger.info("context_built", selected_chunks=len(selected), total_tokens=used_tokens)
        return context, selected
