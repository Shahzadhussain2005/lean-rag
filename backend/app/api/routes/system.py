from __future__ import annotations
from fastapi import APIRouter
from app.models.schemas import CacheStatsResponse, HealthResponse
from app.services.cache.semantic_cache import get_semantic_cache

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", version="1.0.0", environment="development")


@router.get("/cache/stats", response_model=CacheStatsResponse)
def cache_stats() -> CacheStatsResponse:
    stats = get_semantic_cache().get_stats()
    return CacheStatsResponse(
        total_entries=stats.total_entries,
        hit_count=stats.hit_count,
        miss_count=stats.miss_count,
        hit_rate_pct=stats.hit_rate_pct,
        estimated_tokens_saved=stats.estimated_tokens_saved,
    )


@router.delete("/cache", status_code=200)
def clear_cache() -> dict:
    from app.services.cache import semantic_cache as _mod
    _mod._instance = None
    return {"message": "Cache cleared"}