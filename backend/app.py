from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.upload import router as upload_router
from backend.routes.chat import router as chat_router
from backend.routes.documents import router as document_router

app = FastAPI(
    title="Smart Document RAG API",
    description="Hỏi đáp tài liệu thông minh bằng LlamaIndex + ChromaDB + Ollama",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)


@app.get("/")
def root():
    return {
        "message": "Smart Document RAG API is running",
        "docs": "/docs",
        "stack": ["FastAPI", "LlamaIndex", "ChromaDB", "Ollama"],
    }
