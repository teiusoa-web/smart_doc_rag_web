import shutil
from pathlib import Path

from fastapi import UploadFile

from backend.config import DOCS_DIR


async def save_upload_file(file: UploadFile) -> Path:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = Path(file.filename).name
    saved_path = DOCS_DIR / safe_name

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return saved_path


def list_documents():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    return [
        {
            "filename": item.name,
            "path": str(item),
            "size": item.stat().st_size,
        }
        for item in DOCS_DIR.iterdir()
        if item.is_file() and item.name != ".gitkeep"
    ]


def clear_documents():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    for item in DOCS_DIR.iterdir():
        if item.is_file() and item.name != ".gitkeep":
            item.unlink()
