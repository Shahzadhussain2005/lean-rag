from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.domain import DocumentStatus


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    status: DocumentStatus
    created_at: datetime
    chunk_count: int
    total_tokens: int
    error_message: Optional[str] = None


class DocumentListResponse(BaseModel):
    documents: list[DocumentResponse]
    total: int


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    document_id: Optional[str] = None
    top_k: Optional[int] = Field(default=None, ge=1, le=10)


class SourceChunk(BaseModel):
    chunk_id: str
    document_id: str
    text: str
    score: float
    chunk_index: int


class CostMetricsResponse(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cache_hit: bool
    chunks_retrieved: int
    query_compressed: bool
    estimated_savings_pct: float


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    cost_metrics: CostMetricsResponse
    cached: bool


class CacheStatsResponse(BaseModel):
    total_entries: int
    hit_count: int
    miss_count: int
    hit_rate_pct: float
    estimated_tokens_saved: int


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
