cd "D:\DoAn_Rag_web\smart_doc_rag_web"
Set-ExecutionPolicy Bypass -Scope Process -Force
.\.venv\Scripts\Activate.ps1
Write-Host "Backend starting..." -ForegroundColor Green
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
