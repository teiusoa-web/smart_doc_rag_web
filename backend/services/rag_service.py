import shutil
from pathlib import Path

import chromadb
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader, StorageContext
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


def setup_llamaindex():
    Settings.embed_model = OllamaEmbedding(model_name=EMBED_MODEL)
    Settings.llm = Ollama(model=LLM_MODEL, request_timeout=180.0)


def get_chroma_collection():
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    return collection


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

    reader = SimpleDirectoryReader(input_files=[str(file_path)])
    documents = reader.load_data()

    collection = get_chroma_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=Settings.embed_model,
    )

    return {
        "document_count": len(documents),
        "vector_database": "ChromaDB",
        "rag_framework": "LlamaIndex",
        "embedding_model": EMBED_MODEL,
    }


def ask_document(question: str):
    index = get_index()

    query_engine = index.as_query_engine(
        llm=Settings.llm,
        similarity_top_k=SIMILARITY_TOP_K,
    )

    response = query_engine.query(question)

    return str(response)


def clear_vector_database():
    if CHROMA_DIR.exists():
        shutil.rmtree(CHROMA_DIR)

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
