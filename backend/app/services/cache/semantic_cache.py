from __future__ import annotations
import time
import math
from dataclasses import dataclass, field
from typing import Optional
from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.domain import QueryResult

logger = get_logger(__name__)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x * x for x in a))
    mag_b = math.sqrt(sum(x * x for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


@dataclass
class CacheEntry:
    query_embedding: list[float]
    result: QueryResult
    created_at: float = field(default_factory=time.time)


@dataclass
class CacheStats:
    total_entries: int
    hit_count: int
    miss_count: int
    estimated_tokens_saved: int

    @property
    def hit_rate_pct(self) -> float:
        total = self.hit_count + self.miss_count
        return round((self.hit_count / total) * 100, 2) if total > 0 else 0.0


class SemanticCache:
    def __init__(self) -> None:
        settings = get_settings()
        self._ttl = settings.semantic_cache_ttl_seconds
        self._threshold = settings.semantic_cache_similarity_threshold
        self._entries: list[CacheEntry] = []
        self._hit_count = 0
        self._miss_count = 0
        self._tokens_saved = 0

    def lookup(self, query_embedding: list[float]) -> Optional[QueryResult]:
        self._evict_expired()

        best_score = 0.0
        best_entry: Optional[CacheEntry] = None

        for entry in self._entries:
            score = _cosine_similarity(query_embedding, entry.query_embedding)
            if score > best_score:
                best_score = score
                best_entry = entry

        if best_entry and best_score >= self._threshold:
            self._hit_count += 1
            self._tokens_saved += best_entry.result.cost_metrics.total_tokens
            logger.info("cache_hit", similarity=round(best_score, 4), tokens_saved=best_entry.result.cost_metrics.total_tokens)
            return best_entry.result

        self._miss_count += 1
        return None

    def store(self, query_embedding: list[float], result: QueryResult) -> None:
        self._evict_expired()
        self._entries.append(CacheEntry(query_embedding=query_embedding, result=result))
        logger.info("cache_stored", total_entries=len(self._entries))

    def get_stats(self) -> CacheStats:
        self._evict_expired()
        return CacheStats(
            total_entries=len(self._entries),
            hit_count=self._hit_count,
            miss_count=self._miss_count,
            estimated_tokens_saved=self._tokens_saved,
        )

    def _evict_expired(self) -> None:
        now = time.time()
        before = len(self._entries)
        self._entries = [e for e in self._entries if now - e.created_at < self._ttl]
        evicted = before - len(self._entries)
        if evicted:
            logger.debug("cache_eviction", evicted=evicted)


_instance: SemanticCache | None = None


def get_semantic_cache() -> SemanticCache:
    global _instance
    if _instance is None:
        _instance = SemanticCache()
    return _instance
