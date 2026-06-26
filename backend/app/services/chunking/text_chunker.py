from __future__ import annotations
import re
from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.domain import Chunk

logger = get_logger(__name__)


def _estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _split_into_sentences(text: str) -> list[str]:
    pattern = r"(?<=[.!?])\s+(?=[A-Z])"
    sentences = re.split(pattern, text.strip())
    return [s.strip() for s in sentences if s.strip()]


class TextChunker:
    def __init__(self) -> None:
        settings = get_settings()
        self._chunk_size = settings.chunk_size
        self._chunk_overlap = settings.chunk_overlap

    def chunk(self, document_id: str, text: str) -> list[Chunk]:
        text = self._normalize(text)
        sentences = _split_into_sentences(text)

        chunks: list[Chunk] = []
        current_sentences: list[str] = []
        current_tokens = 0
        chunk_index = 0

        for sentence in sentences:
            sentence_tokens = _estimate_tokens(sentence)

            if current_tokens + sentence_tokens > self._chunk_size and current_sentences:
                chunk_text = " ".join(current_sentences)
                chunks.append(
                    Chunk.create(
                        document_id=document_id,
                        text=chunk_text,
                        index=chunk_index,
                        token_count=current_tokens,
                    )
                )
                chunk_index += 1

                overlap_sentences: list[str] = []
                overlap_tokens = 0
                for s in reversed(current_sentences):
                    t = _estimate_tokens(s)
                    if overlap_tokens + t <= self._chunk_overlap:
                        overlap_sentences.insert(0, s)
                        overlap_tokens += t
                    else:
                        break

                current_sentences = overlap_sentences
                current_tokens = overlap_tokens

            current_sentences.append(sentence)
            current_tokens += sentence_tokens

        if current_sentences:
            chunk_text = " ".join(current_sentences)
            chunks.append(
                Chunk.create(
                    document_id=document_id,
                    text=chunk_text,
                    index=chunk_index,
                    token_count=current_tokens,
                )
            )

        logger.info("document_chunked", document_id=document_id, chunk_count=len(chunks))
        return chunks

    @staticmethod
    def _normalize(text: str) -> str:
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        return text.strip()
