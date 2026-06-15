from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from backend.services.rag_service import ask_document

router = APIRouter(tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Câu hỏi không được để trống")

    answer = ask_document(question)

    return {
        "question": question,
        "answer": answer,
    }
