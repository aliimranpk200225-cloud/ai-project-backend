from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes.chat import router as chat_router
from app.core.startup import load_vector_store
from app.services.memory_service import MemoryService


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting application...")

    load_vector_store()

    yield

    print("Application shutting down...")

app = FastAPI(
    title="AI RAG Backend",
    lifespan=lifespan
)

app.include_router(chat_router)


# memory_service = MemoryService()