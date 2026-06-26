from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class DocumentStatus(str, Enum):
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


@dataclass
class Chunk:
    id: str
    document_id: str
    text: str
    index: int
    token_count: int
    embedding: Optional[list[float]] = None

    @classmethod
    def create(cls, document_id: str, text: str, index: int, token_count: int) -> "Chunk":
        return cls(
            id=str(uuid.uuid4()),
            document_id=document_id,
            text=text,
            index=index,
            token_count=token_count,
        )


@dataclass
class Document:
    id: str
    filename: str
    content_type: str
    status: DocumentStatus
    created_at: datetime
    chunk_count: int = 0
    total_tokens: int = 0
    error_message: Optional[str] = None

    @classmethod
    def create(cls, filename: str, content_type: str) -> "Document":
        return cls(
            id=str(uuid.uuid4()),
            filename=filename,
            content_type=content_type,
            status=DocumentStatus.PROCESSING,
            created_at=datetime.utcnow(),
        )


@dataclass
class RetrievedChunk:
    chunk: Chunk
    score: float


@dataclass
class CostMetrics:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cache_hit: bool = False
    chunks_retrieved: int = 0
    query_compressed: bool = False
    estimated_savings_pct: float = 0.0


@dataclass
class QueryResult:
    answer: str
    sources: list[RetrievedChunk]
    cost_metrics: CostMetrics
    cached: bool = False
