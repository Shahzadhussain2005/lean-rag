from __future__ import annotations
from fastapi import APIRouter, HTTPException, status
from app.core.exceptions import DocumentNotFoundError, EmbeddingError, LLMError
from app.models.schemas import CostMetricsResponse, QueryRequest, QueryResponse, SourceChunk
from app.services.rag.factory import get_rag_pipeline

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
async def query_documents(body: QueryRequest) -> QueryResponse:
    pipeline = get_rag_pipeline()

    try:
        result = await pipeline.query(
            question=body.question,
            document_id=body.document_id,
            top_k=body.top_k,
        )
    except DocumentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    except EmbeddingError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Embedding service error: {exc}")
    except LLMError as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"LLM error: {exc}")

    return QueryResponse(
        answer=result.answer,
        sources=[
            SourceChunk(
                chunk_id=rc.chunk.id,
                document_id=rc.chunk.document_id,
                text=rc.chunk.text,
                score=round(rc.score, 4),
                chunk_index=rc.chunk.index,
            )
            for rc in result.sources
        ],
        cost_metrics=CostMetricsResponse(
            prompt_tokens=result.cost_metrics.prompt_tokens,
            completion_tokens=result.cost_metrics.completion_tokens,
            total_tokens=result.cost_metrics.total_tokens,
            cache_hit=result.cost_metrics.cache_hit,
            chunks_retrieved=result.cost_metrics.chunks_retrieved,
            query_compressed=result.cost_metrics.query_compressed,
            estimated_savings_pct=result.cost_metrics.estimated_savings_pct,
        ),
        cached=result.cached,
    )
