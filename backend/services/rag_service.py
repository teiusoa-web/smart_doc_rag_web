import shutil
from pathlib import Path

import chromadb
import pdfplumber

from pdf2image import convert_from_path
from rapidocr_onnxruntime import RapidOCR

from docx import Document as DocxDocument

from llama_index.core import Settings, VectorStoreIndex, StorageContext
from llama_index.core.schema import Document
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from backend.config import (
    CHROMA_DIR,
    COLLECTION_NAME,
    EMBED_MODEL,
    LLM_MODEL,
    SIMILARITY_TOP_K,
)


def read_pdf_with_ocr(file_path: Path) -> str:
    ocr = RapidOCR()
    pages = convert_from_path(str(file_path), dpi=200)

    text_parts = []

    for page_number, image in enumerate(pages, start=1):
        result, _ = ocr(image)

        page_text = ""

        if result:
            for line in result:
                page_text += line[1] + "\n"

        if page_text.strip():
            text_parts.append(f"\n--- Trang {page_number} OCR ---\n{page_text}")

    return "\n".join(text_parts).strip()

def setup_llamaindex():
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=180.0)
    Settings.text_splitter = SentenceSplitter(
        chunk_size=512,
        chunk_overlap=80,
    )


def read_pdf_with_pdfplumber(file_path: Path) -> str:
    text_parts = []

    with pdfplumber.open(str(file_path)) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""

            if page_text.strip():
                text_parts.append(f"\n--- Trang {page_number} ---\n{page_text}")

    return "\n".join(text_parts).strip()


def read_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


def read_document_text(file_path: Path) -> str:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        text = read_pdf_with_pdfplumber(file_path)

        if is_good_text(text):
            return text

        print("PDF extract lỗi, chuyển OCR...")
        return read_pdf_with_ocr(file_path)

    elif suffix == ".docx":
        return read_docx(file_path)

    elif suffix == ".txt":
        return read_txt(file_path)

    raise ValueError(
        "Chỉ hỗ trợ PDF, DOCX và TXT"
    )

def read_docx(file_path: Path) -> str:
    doc = DocxDocument(str(file_path))

    paragraphs = []

    for para in doc.paragraphs:
        if para.text.strip():
            paragraphs.append(para.text)

    return "\n".join(paragraphs)

def is_good_text(text: str) -> bool:
    if not text or len(text.strip()) < 50:
        return False

    readable_chars = sum(
        1 for char in text
        if char.isalnum() or char.isspace() or char in ".,;:!?()[]{}+-=*/_@#$%&<>"
    )

    ratio = readable_chars / max(len(text), 1)

    return ratio > 0.75

def get_chroma_collection():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    return client.get_or_create_collection(COLLECTION_NAME)


def get_index():
    setup_llamaindex()

    collection = get_chroma_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)

    return VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=Settings.embed_model,
    )


def index_document(file_path: Path):
    setup_llamaindex()

    if not file_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {file_path}")

    text = read_document_text(file_path)

    print("=" * 60)
    print("FILE:", file_path.name)
    print("TEXT LENGTH:", len(text))
    print("TEXT PREVIEW:")
    print(text[:3000])
    print("=" * 60)

    if not text or len(text.strip()) < 20:
        raise ValueError(
            "Không đọc được nội dung PDF. File này có thể là PDF scan ảnh, cần OCR."
        )

    document = Document(
        text=text,
        metadata={
            "file_name": file_path.name,
            "file_path": str(file_path),
        },
    )

    collection = get_chroma_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)

    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )

    VectorStoreIndex.from_documents(
        [document],
        storage_context=storage_context,
        embed_model=Settings.embed_model,
        show_progress=True,
    )

    return {
        "document_count": 1,
        "text_length": len(text),
        "vector_database": "ChromaDB",
        "rag_framework": "LlamaIndex",
        "pdf_reader": "pdfplumber",
        "embedding_model": EMBED_MODEL,
        "llm_model": LLM_MODEL,
    }


def ask_document(question: str):
    setup_llamaindex()

    index = get_index()

    retriever = index.as_retriever(
        similarity_top_k=SIMILARITY_TOP_K
    )

    nodes = retriever.retrieve(question)

    if not nodes:
        return {
            "answer": "Không tìm thấy thông tin này trong tài liệu.",
            "sources": []
        }

    context = "\n\n".join([node.text for node in nodes])

    prompt = f"""
Bạn là chatbot hỏi đáp tài liệu.

Chỉ sử dụng thông tin trong tài liệu để trả lời.

Quy tắc:
- Trả lời trực tiếp câu hỏi.
- Không nhắc tới từ "NGỮ CẢNH".
- Không nói "Theo ngữ cảnh".
- Trả lời tự nhiên bằng tiếng Việt.
- Nếu không có thông tin thì trả lời:
  "Không tìm thấy thông tin này trong tài liệu."

Tài liệu:
{context}

Câu hỏi:
{question}
"""

    response = Settings.llm.complete(prompt)

    sources = []

    for i, node in enumerate(nodes, start=1):
        sources.append({
            "index": i,
            "score": float(node.score) if node.score else None,
            "preview": node.text[:300]
        })

    return {
        "answer": str(response),
        "sources": sources
    }


def clear_vector_database():
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)