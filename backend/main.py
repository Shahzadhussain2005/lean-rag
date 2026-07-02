import uvicorn
from app.app import create_app
from app.core.config import get_settings

app = create_app()

@app.on_event("startup")
async def preload_models():
    from app.services.embedding.embedding_service import get_embedding_service
    get_embedding_service()

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.is_development,
        log_level="debug" if settings.is_development else "info",
    )