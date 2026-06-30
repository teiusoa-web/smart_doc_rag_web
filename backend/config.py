from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "docs"
CHROMA_DIR = DATA_DIR / "chroma_db"

COLLECTION_NAME = "smart_documents"

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"

SIMILARITY_TOP_K = 6

PARENT_CHUNK_SIZE = 1500
PARENT_CHUNK_OVERLAP = 300
CHILD_CHUNK_SIZE = 300
CHILD_CHUNK_OVERLAP = 50
SOURCE_SCORE_THRESHOLD = 0.15
