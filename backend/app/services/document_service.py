from __future__ import annotations
from typing import Optional
from app.core.exceptions import DocumentNotFoundError
from app.core.logging import get_logger
from app.models.domain import Document, DocumentStatus
from app.services.chunking.document_parser import parse_document
from app.services.chunking.text_chunker import TextChunker
from app.services.embedding.embedding_service import EmbeddingService
from app.services.vector_store.vector_store import VectorStore

logger = get_logger(__name__)


class DocumentService:
    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._chunker = TextChunker()
        self._documents: dict[str, Document] = {}

    async def ingest(self, file_bytes: bytes, filename: str, content_type: str) -> Document:
        doc = Document.create(filename=filename, content_type=content_type)
        self._documents[doc.id] = doc
        logger.info("document_ingestion_started", document_id=doc.id, filename=filename)

        try:
            text = await parse_document(file_bytes, content_type, filename)
            chunks = self._chunker.chunk(doc.id, text)

            texts = [c.text for c in chunks]
            embeddings = self._embedding_service.embed_texts(texts)

            for chunk, embedding in zip(chunks, embeddings):
                chunk.embedding = embedding

            self._vector_store.upsert_chunks(chunks)

            doc.status = DocumentStatus.READY
            doc.chunk_count = len(chunks)
            doc.total_tokens = sum(c.token_count for c in chunks)
            logger.info("document_ingestion_complete", document_id=doc.id, chunks=doc.chunk_count)

        except Exception as exc:
            doc.status = DocumentStatus.FAILED
            doc.error_message = str(exc)
            logger.error("document_ingestion_failed", document_id=doc.id, error=str(exc))

        return doc

    def get(self, document_id: str) -> Document:
        doc = self._documents.get(document_id)
        if doc is None:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        return doc

    def list_all(self) -> list[Document]:
        return list(self._documents.values())

    def delete(self, document_id: str) -> None:
        if document_id not in self._documents:
            raise DocumentNotFoundError(f"Document {document_id} not found")
        self._vector_store.delete_document(document_id)
        del self._documents[document_id]
        logger.info("document_deleted", document_id=document_id)


_instance: Optional[DocumentService] = None


def get_document_service() -> DocumentService:
    global _instance
    if _instance is None:
        from app.services.embedding.embedding_service import get_embedding_service
        from app.services.vector_store.vector_store import get_vector_store
        _instance = DocumentService(
            embedding_service=get_embedding_service(),
            vector_store=get_vector_store(),
        )
    return _instance