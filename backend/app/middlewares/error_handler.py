from __future__ import annotations
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
    DocumentNotFoundError,
    DocumentParsingError,
    EmbeddingError,
    LLMError,
    RAGBaseException,
    UnsupportedFileTypeError,
)
from app.core.logging import get_logger

logger = get_logger(__name__)


async def rag_exception_handler(request: Request, exc: RAGBaseException) -> JSONResponse:
    status_map = {
        DocumentNotFoundError: 404,
        UnsupportedFileTypeError: 415,
        DocumentParsingError: 422,
        EmbeddingError: 502,
        LLMError: 502,
    }
    status_code = status_map.get(type(exc), 500)
    logger.warning("handled_exception", exc_type=type(exc).__name__, detail=str(exc), path=str(request.url))
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_exception", exc_type=type(exc).__name__, detail=str(exc), path=str(request.url))
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred."})
