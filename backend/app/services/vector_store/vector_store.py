from __future__ import annotations
import math
from typing import Optional
from app.core.exceptions import VectorStoreError
from app.core.logging import get_logger
from app.models.domain import Chunk, RetrievedChunk

logger = get_logger(__name__)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


class VectorStore:
    def __init__(self) -> None:
        self._chunks: dict[str, Chunk] = {}
        self._document_index: dict[str, list[str]] = {}

    def upsert_chunks(self, chunks: list[Chunk]) -> None:
        for chunk in chunks:
            if chunk.embedding is None:
                raise VectorStoreError(f"Chunk {chunk.id} has no embedding")
            self._chunks[chunk.id] = chunk
            self._document_index.setdefault(chunk.document_id, []).append(chunk.id)

        logger.info("chunks_upserted", count=len(chunks))

    def search(
        self,
        query_embedding: list[float],
        top_k: int,
        document_id: Optional[str] = None,
    ) -> list[RetrievedChunk]:
        candidates = self._get_candidate_chunks(document_id)

        if not candidates:
            return []

        scored = [
            RetrievedChunk(chunk=chunk, score=_cosine_similarity(query_embedding, chunk.embedding))  # type: ignore[arg-type]
            for chunk in candidates
            if chunk.embedding is not None
        ]

        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

    def delete_document(self, document_id: str) -> int:
        chunk_ids = self._document_index.pop(document_id, [])
        for cid in chunk_ids:
            self._chunks.pop(cid, None)
        logger.info("document_deleted_from_store", document_id=document_id, chunks_removed=len(chunk_ids))
        return len(chunk_ids)

    def get_document_chunk_count(self, document_id: str) -> int:
        return len(self._document_index.get(document_id, []))

    def _get_candidate_chunks(self, document_id: Optional[str]) -> list[Chunk]:
        if document_id:
            ids = self._document_index.get(document_id, [])
            return [self._chunks[cid] for cid in ids if cid in self._chunks]
        return list(self._chunks.values())


_instance: VectorStore | None = None


def get_vector_store() -> VectorStore:
    global _instance
    if _instance is None:
        _instance = VectorStore()
    return _instance
