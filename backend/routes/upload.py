from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.services.document_service import save_upload_file
from backend.services.rag_service import index_document

router = APIRouter(tags=["Upload"])


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="File không hợp lệ")

    lower_name = file.filename.lower()

    if not lower_name.endswith((".pdf", ".txt", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Chỉ hỗ trợ file PDF, TXT hoặc DOCX"
        )

    saved_path = await save_upload_file(file)
    result = index_document(saved_path)

    return {
        "message": "Upload và index tài liệu thành công",
        "filename": file.filename,
        "saved_path": str(saved_path),
        "indexed": result,
    }