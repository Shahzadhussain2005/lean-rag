from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import documents, query, system
from app.core.exceptions import RAGBaseException
from app.core.logging import configure_logging
from app.middlewares.error_handler import rag_exception_handler, unhandled_exception_handler


def create_app() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title="RAG API",
        description="Production-grade Retrieval-Augmented Generation with cost optimization",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_exception_handler(RAGBaseException, rag_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(Exception, unhandled_exception_handler)

    app.include_router(system.router)
    app.include_router(documents.router, prefix="/api/v1")
    app.include_router(query.router, prefix="/api/v1")

    return app
