from __future__ import annotations
from typing import Optional
from app.services.cache.semantic_cache import get_semantic_cache
from app.services.embedding.embedding_service import get_embedding_service
from app.services.rag.context_builder import ContextBuilder
from app.services.rag.query_compressor import get_query_compressor
from app.services.rag.rag_pipeline import RAGPipeline
from app.services.vector_store.vector_store import get_vector_store

_instance: Optional[RAGPipeline] = None


def get_rag_pipeline() -> RAGPipeline:
    global _instance
    if _instance is None:
        _instance = RAGPipeline(
            embedding_service=get_embedding_service(),
            vector_store=get_vector_store(),
            semantic_cache=get_semantic_cache(),
            query_compressor=get_query_compressor(),
            context_builder=ContextBuilder(),
        )
    return _instance
