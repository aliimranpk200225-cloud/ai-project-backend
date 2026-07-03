# app/core/startup.py

from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService

embedding_service = EmbeddingService()
vector_service = VectorStoreService()

vector_store = None
retriever = None


def load_vector_store():
    global vector_store
    global retriever

    vector_store = vector_service.load_vector_store(
        embedding_service.get_model()
    )

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    print("✅ FAISS loaded successfully")