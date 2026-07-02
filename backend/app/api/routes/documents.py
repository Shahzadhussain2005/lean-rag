from __future__ import annotations
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from app.core.exceptions import DocumentNotFoundError, UnsupportedFileTypeError
from app.models.schemas import DocumentListResponse, DocumentResponse
from app.services.document_service import get_document_service

router = APIRouter(prefix="/documents", tags=["documents"])

_ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "text/markdown",
}

_MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(file: UploadFile = File(...)) -> DocumentResponse:
    if file.content_type not in _ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type '{file.content_type}'. Allowed: PDF, DOCX, TXT, MD.",
        )

    file_bytes = await file.read()

    if len(file_bytes) > _MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File exceeds 20 MB limit.",
        )

    service = get_document_service()
    doc = await service.ingest(file_bytes, file.filename or "untitled", file.content_type)

    return _to_response(doc)


@router.get("", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    service = get_document_service()
    docs = service.list_all()
    return DocumentListResponse(
        documents=[_to_response(d) for d in docs],
        total=len(docs),
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str) -> DocumentResponse:
    try:
        doc = get_document_service().get(document_id)
        return _to_response(doc)
    except DocumentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")


@router.delete("/{document_id}", status_code=status.HTTP_200_OK)
def delete_document(document_id: str) -> dict:
    try:
        get_document_service().delete(document_id)
        return {"message": "Document deleted successfully"}
    except DocumentNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")

def _to_response(doc) -> DocumentResponse:
    return DocumentResponse(
        id=doc.id,
        filename=doc.filename,
        content_type=doc.content_type,
        status=doc.status,
        created_at=doc.created_at,
        chunk_count=doc.chunk_count,
        total_tokens=doc.total_tokens,
        error_message=doc.error_message,
    )
