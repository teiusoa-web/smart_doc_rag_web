from fastapi import APIRouter

from backend.services.document_service import list_documents, clear_documents
from backend.services.rag_service import clear_vector_database

router = APIRouter(tags=["Documents"])


@router.get("/documents")
def get_documents():
    return {
        "documents": list_documents(),
    }


@router.delete("/documents")
def delete_documents():
    clear_documents()
    clear_vector_database()

    return {
        "message": "Đã xóa tài liệu và ChromaDB",
    }
