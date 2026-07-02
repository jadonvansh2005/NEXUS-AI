from fastapi import APIRouter

from api.routes.chat import (
    router as chat_router
)

from api.routes.rag import (
    router as rag_router
)

api_router = APIRouter()

api_router.include_router(
    chat_router,
    tags=["Chat"]
)

api_router.include_router(
    rag_router,
    prefix="/rag",
    tags=["RAG"]
)