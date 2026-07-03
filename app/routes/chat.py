from fastapi import APIRouter

from app.schemas.chat import ChatResponse, ChatRequest
from app.services.memory_service import memory_service
from app.services.gemini_service import GeminiService
from app.services.pdf_service import PdfService
from app.services.vector_store_service import VectorStoreService
from app.services.embedding_service import EmbeddingService
from app.services.retriever_service import RetrieverService
from app.core import startup
from app.services.rag_service import RAGService
gemini_service = GeminiService()
retriever_service = RetrieverService()
vector_service = VectorStoreService()
embedding_service = EmbeddingService()
pdf_service = PdfService()
router = APIRouter()

gemini = GeminiService()
@router.get("/pdf")
def read_pdf():

    docs = pdf_service.load_pdf("data/sample.pdf")

    return {
        "pages": len(docs),
        "first_page": docs[0].page_content[:500],
        "metadata": docs[0].metadata
    }
@router.get("/chunks")
def chunks():

    docs = pdf_service.load_pdf("data/sample.pdf")

    chunks = pdf_service.split_documents(docs)

    return {
        "documents": len(docs),
        "chunks": len(chunks),
        "first_chunk": chunks[0].page_content,
        "metadata": chunks[0].metadata
    }
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = gemini.ask(request.question)
    return ChatResponse(answer=answer)

@router.get("/vector-store")
def build_vector_store():

    docs = pdf_service.load_pdf("data/sample.pdf")

    chunks = pdf_service.split_documents(docs)

    vector_store = vector_service.create_vector_store(
        chunks,
        embedding_service.get_model()
    )

    return {
        "documents": len(docs),
        "chunks": len(chunks),
        "status": "Vector Store Created Successfully"
    }




@router.get("/retrieve")
def retrieve():

    docs = pdf_service.load_pdf("data/sample.pdf")

    chunks = pdf_service.split_documents(docs)

    vector_store = vector_service.create_vector_store(
        chunks,
        embedding_service.get_model()
    )

    retriever = retriever_service.create_retriever(vector_store)

    results = retriever.invoke("What is sheikhupura?")

    return {
        "results": [
            {
                "page": doc.metadata.get("page"),
                "text": doc.page_content
            }
            for doc in results
        ]
    }
from app.services.gemini_service import GeminiService


@router.post("/ask")
def ask(request: ChatRequest):


    rag_service = RAGService(
        startup.retriever,
        gemini_service.llm
    )

    history = memory_service.get_history(request.session_id)
    formatted_history = format_history(history)
    chain = rag_service.build_chain()

    answer = chain.invoke(
        {
            "question": request.question,
            "history": formatted_history
        }
    )
    memory_service.add_user_message(
        request.session_id,
        request.question
    )
    memory_service.add_ai_message(
        request.session_id,
        answer
    )

    return {
        "answer": answer
    }
def format_history(history):

    formatted = ""

    for message in history:

        formatted += f"{message['role']}: {message['content']}\n"

    return formatted
@router.post("/build-index")
def build_index():

    documents = pdf_service.load_pdf("data/sample.pdf")

    chunks = pdf_service.split_documents(documents)

    vector_store = vector_service.create_vector_store(
        chunks,
        embedding_service.get_model()
    )

    vector_service.save_vector_store(vector_store)

    return {
        "message": "FAISS index created successfully."
    }