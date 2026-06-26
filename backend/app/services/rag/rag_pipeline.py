from __future__ import annotations
from typing import Optional
from groq import AsyncGroq
from app.core.config import get_settings
from app.core.exceptions import LLMError
from app.core.logging import get_logger
from app.models.domain import CostMetrics, QueryResult
from app.services.cache.semantic_cache import SemanticCache
from app.services.embedding.embedding_service import EmbeddingService
from app.services.rag.context_builder import ContextBuilder
from app.services.rag.query_compressor import QueryCompressor
from app.services.vector_store.vector_store import VectorStore

logger = get_logger(__name__)

_SYSTEM_PROMPT = (
    "You are a precise question-answering assistant. Answer the user's question "
    "using only the provided context. If the answer is not in the context, say so clearly. "
    "Be concise and cite source numbers where relevant."
)


class RAGPipeline:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        semantic_cache: SemanticCache,
        query_compressor: QueryCompressor,
        context_builder: ContextBuilder,
    ) -> None:
        settings = get_settings()
        self._client = AsyncGroq(api_key=settings.groq_api_key)
        self._model = settings.llm_model
        self._top_k = settings.max_retrieved_chunks
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._cache = semantic_cache
        self._compressor = query_compressor
        self._context_builder = context_builder

    async def query(self, question: str, document_id: Optional[str] = None, top_k: Optional[int] = None) -> QueryResult:
        effective_top_k = top_k or self._top_k

        raw_embedding = self._embedding_service.embed_query(question)

        cached = self._cache.lookup(raw_embedding)
        if cached:
            cached.cached = True
            return cached

        compressed_query, was_compressed = await self._compressor.compress(question)

        search_embedding = (
            self._embedding_service.embed_query(compressed_query)
            if was_compressed
            else raw_embedding
        )

        retrieved = self._vector_store.search(
            query_embedding=search_embedding,
            top_k=effective_top_k,
            document_id=document_id,
        )

        context, selected_chunks = self._context_builder.build(retrieved)

        answer, usage = await self._call_llm(question, context)

        cost_metrics = CostMetrics(
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            cache_hit=False,
            chunks_retrieved=len(selected_chunks),
            query_compressed=was_compressed,
            estimated_savings_pct=self._estimate_savings(was_compressed, len(selected_chunks), effective_top_k),
        )

        result = QueryResult(
            answer=answer,
            sources=selected_chunks,
            cost_metrics=cost_metrics,
            cached=False,
        )

        self._cache.store(raw_embedding, result)
        return result

    async def _call_llm(self, question: str, context: str) -> tuple[str, dict]:
        user_message = f"Context:\n{context}\n\nQuestion: {question}"
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.1,
                max_tokens=1024,
            )
            content = response.choices[0].message.content or ""
            usage = {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            }
            return content, usage
        except Exception as exc:
            logger.error("llm_call_failed", error=str(exc))
            raise LLMError(f"LLM call failed: {exc}") from exc

    @staticmethod
    def _estimate_savings(compressed: bool, used_chunks: int, max_chunks: int) -> float:
        savings = 0.0
        if compressed:
            savings += 15.0
        if used_chunks < max_chunks:
            savings += ((max_chunks - used_chunks) / max_chunks) * 20.0
        return round(min(savings, 60.0), 1)