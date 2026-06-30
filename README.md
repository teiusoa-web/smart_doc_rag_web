# Document RAG Web

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-RAG-orange)
![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-purple)
![Ollama](https://img.shields.io/badge/Ollama-LocalLLM-black)
![Llama3.2](https://img.shields.io/badge/Llama-3.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

Hệ thống hỏi đáp tài liệu thông minh sử dụng RAG (Retrieval-Augmented Generation) với LlamaIndex, ChromaDB và Ollama.

## ✨ Tính năng

- ✅ Upload tài liệu (PDF, DOCX, TXT)
- ✅ Xử lý PDF với OCR (tự động fallback)
- ✅ Tạo vector embedding tự động
- ✅ Lưu vector bằng ChromaDB
- ✅ Hỏi đáp dựa trên nội dung tài liệu
- ✅ Hiển thị nguồn tham khảo
- ✅ Lưu lịch sử chat trên browser
- ✅ Giao diện tiếng Việt
- ✅ Chạy 100% local (không cần API keys)

---

## 🛠️ Công nghệ sử dụng

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Bootstrap 5** - CSS framework
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### AI & RAG
- **LlamaIndex** - RAG framework
- **ChromaDB** - Vector database
- **Ollama** - Local LLM runtime
- **nomic-embed-text** - Embedding model
- **Llama 3.2** - LLM model

### Document Processing
- **pdfplumber** - PDF text extraction
- **RapidOCR** - Image-based text recognition
- **python-docx** - DOCX support

---

## 📋 Yêu cầu hệ thống

- **Python 3.10+**
- **Node.js 16+**
- **Ollama** (https://ollama.ai)
- **RAM**: Tối thiểu 8GB (tốt nhất 16GB+)
- **GPU**: Tùy chọn (tăng tốc độ)

---

## ⚙️ Hướng dẫn cài đặt

### 1️⃣ Cài đặt Ollama

Tải xuống từ: https://ollama.ai

Hoặc trên Linux:
```bash
curl https://ollama.ai/install.sh | sh
```

### 2️⃣ Clone hoặc setup project

```bash
# Nếu chưa có project
git clone <repo-url>
cd smart_doc_rag_web

# Hoặc nếu đã có
cd smart_doc_rag_web
```

### 3️⃣ Chạy script setup (Windows PowerShell)

```bash
.\setup.ps1
```

Hoặc setup thủ công:

```bash
# Tạo venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Cài backend
pip install -r backend/requirements.txt

# Cài frontend
cd frontend
npm install
cd ..
```

### 4️⃣ Tải Ollama models

```bash
# Mở terminal mới
ollama serve

# Terminal khác - tải models
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 5️⃣ Chạy ứng dụng

**Cách 1: Tự động (Windows PowerShell)**
```bash
.\run_all.ps1
```

**Cách 2: Thủ công**

Terminal 1 - Ollama (nếu chưa chạy):
```bash
ollama serve
```

Terminal 2 - Backend:
```bash
.\.venv\Scripts\Activate.ps1
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```

Terminal 3 - Frontend:
```bash
cd frontend
npm run dev
```

### 6️⃣ Truy cập ứng dụng

- **Frontend**: http://127.0.0.1:5173
- **API Docs**: http://127.0.0.1:8000/docs
- **Swagger UI**: http://127.0.0.1:8000/swagger_ui

---

## 📁 Cấu trúc thư mục

```
smart_doc_rag_web/
│
├── backend/                          # Backend FastAPI
│   ├── app.py                       # Ứng dụng chính
│   ├── config.py                    # Cấu hình
│   │
│   ├── routes/                      # API routes
│   │   ├── upload.py               # Upload tài liệu
│   │   ├── chat.py                 # Chat/QA
│   │   └── documents.py            # Quản lý tài liệu
│   │
│   ├── services/                    # Business logic
│   │   ├── document_service.py     # Xử lý file
│   │   └── rag_service.py          # RAG logic
│   │
│   ├── requirements.txt            # Python dependencies
│   └── __init__.py
│
├── frontend/                         # Frontend React
│   ├── src/
│   │   ├── App.jsx                 # Component chính
│   │   ├── api.js                  # API client
│   │   ├── main.jsx                # Entry point
│   │   └── style.css               # Styles
│   │
│   ├── index.html                  # HTML template
│   ├── package.json                # NPM dependencies
│   ├── vite.config.js              # Vite config
│   ├── .env                        # Environment variables
│   └── .env.example
│
├── data/                            # Data storage
│   ├── docs/                       # Uploaded documents
│   └── chroma_db/                  # Vector database
│
├── setup.ps1                        # Auto setup script
├── verify.ps1                       # Verification script
├── run_all.ps1                      # Run all servers
├── SETUP.md                         # Detailed setup guide
├── README.md                        # This file
└── LICENSE
```

---

## 🚀 Sử dụng ứng dụng

### Quy trình cơ bản

1. **Upload tài liệu**
   - Chọn file PDF/DOCX/TXT
   - Nhấp "Upload & Index"
   - Hệ thống sẽ:
     - Đọc nội dung tài liệu
     - Tạo embedding với nomic-embed-text
     - Lưu vector vào ChromaDB

2. **Hỏi đáp**
   - Nhập câu hỏi về tài liệu
   - Hệ thống sẽ:
     - Tìm đoạn liên quan trong ChromaDB
     - Gửi tới Llama 3.2 để tạo câu trả lời
     - Hiển thị câu trả lời + nguồn tham khảo

3. **Quản lý tài liệu**
   - Xem danh sách tài liệu đã upload
   - Xóa tài liệu hoặc toàn bộ ChromaDB

---

## 📡 API Endpoints

### Health Check
```bash
GET /
```
Response:
```json
{
  "message": "Smart Document RAG API is running",
  "docs": "/docs",
  "stack": ["FastAPI", "LlamaIndex", "ChromaDB", "Ollama"]
}
```

### Upload Document
```bash
POST /upload
Content-Type: multipart/form-data

file: <binary>
```
Response:
```json
{
  "message": "Upload và index tài liệu thành công",
  "filename": "document.pdf",
  "saved_path": "data/docs/document.pdf",
  "indexed": {...}
}
```

### Ask Question
```bash
POST /chat
Content-Type: application/json

{
  "question": "Tài liệu nói gì về X?"
}
```
Response:
```json
{
  "question": "Tài liệu nói gì về X?",
  "answer": "Theo tài liệu, ...",
  "sources": [
    {
      "index": 1,
      "file_name": "document.pdf",
      "page": 5,
      "preview": "...",
      "score": 0.92
    }
  ]
}
```

### Get Documents
```bash
GET /documents
```
Response:
```json
{
  "documents": [
    {
      "filename": "document.pdf",
      "path": "data/docs/document.pdf",
      "size": 1048576
    }
  ]
}
```

### Delete Documents
```bash
DELETE /documents
```
Response:
```json
{
  "message": "Đã xóa tài liệu và ChromaDB"
}
```

---

## 🔧 Cấu hình

### Backend Config (backend/config.py)

```python
CHROMA_DB_PATH = "data/chroma_db"
COLLECTION_NAME = "smart_documents"
EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.2"
SIMILARITY_TOP_K = 6  # Số kết quả lấy từ vector DB
```

### Frontend Config (frontend/.env)

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## 🐛 Troubleshooting

### ❌ Ollama không kết nối

```bash
# Kiểm tra Ollama đang chạy
ollama list

# Nếu lỗi, restart Ollama
ollama serve
```

### ❌ Backend lỗi khi start

```bash
# Xóa cache ChromaDB
rmdir /s data\chroma_db  # Windows
rm -rf data/chroma_db    # Linux/Mac

# Restart backend
python -m uvicorn backend.app:app --reload
```

### ❌ Frontend không load

```bash
# Xóa cache npm
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### ❌ Models chưa tải xuống

```bash
# Chạy lần lượt
ollama pull nomic-embed-text
ollama pull llama3.2

# Kiểm tra
ollama list
```

### ❌ Performance chậm

- Tăng RAM hoặc GPU
- Giảm SIMILARITY_TOP_K
- Dùng model nhỏ hơn (Mistral, Phi)

---

## 📚 Mở rộng

### Thêm models khác

Sửa `backend/config.py`:
```python
LLM_MODEL = "mistral"  # Hoặc: neural-chat, phi, orca-mini
EMBED_MODEL = "nomic-embed-text"  # Hoặc: all-minilm
```

Tải model:
```bash
ollama pull mistral
```

### Thêm document types

Sửa `backend/services/rag_service.py`:
```python
def read_document_text(file_path: Path) -> str:
    # Thêm support cho .xlsx, .pptx, v.v
```

---

## 🤝 Contribute

1. Fork repository
2. Tạo branch: `git checkout -b feature/xyz`
3. Commit changes: `git commit -m "Add xyz"`
4. Push: `git push origin feature/xyz`
5. Tạo Pull Request

---

## 📄 License

MIT License - xem [LICENSE](LICENSE)

---

## 👨‍💻 Author

Tạo bởi Cpeach Team

---

## 🔗 Resources

- [LlamaIndex Docs](https://docs.llamaindex.ai)
- [ChromaDB Docs](https://docs.trychroma.com)
- [Ollama](https://ollama.ai)
- [FastAPI](https://fastapi.tiangolo.com)
- [React](https://react.dev)

---

## 💬 Support

Nếu gặp vấn đề:
1. Kiểm tra [Troubleshooting](#-troubleshooting)
2. Xem [Detailed Setup Guide](SETUP.md)
3. Chạy `.\verify.ps1` để kiểm tra setup
│   ├── src
│   │   ├── App.jsx
│   │   ├── api.js
│   │   └── style.css
│   │
│   ├── package.json
│   └── vite.config.js
│
├── data
│   ├── docs
│   └── chroma_db
│
└── README.md
```

---

## Cài đặt

### Clone project

```bash
git clone https://github.com/teiusoa-web/smart_doc_rag_web.git
cd smart_doc_rag_web
```

### Tạo môi trường ảo

```powershell
python -m venv .venv
```

Kích hoạt:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Cài thư viện backend

```powershell
pip install -r backend/requirements.txt
```

### Cài Ollama

Tải và cài đặt Ollama:

:contentReference[oaicite:0]{index=0}

### Tải model

Embedding:

```powershell
ollama pull nomic-embed-text
```

LLM:

```powershell
ollama pull llama3.2
```

Kiểm tra:

```powershell
ollama list
```

---

## Chạy Backend

```powershell
python -m uvicorn backend.app:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Chạy Frontend

```powershell
cd frontend

npm install

npm run dev
```

Mở:

```text
http://127.0.0.1:5173
```

---

## Luồng hoạt động

### Upload tài liệu

```text
PDF / TXT / DOCX
    │
    ▼
Document Reader
    │
    ▼
Chunking
    │
    ▼
nomic-embed-text
    │
    ▼
ChromaDB
```

### Hỏi đáp

```text
Question
    │
    ▼
Retriever
    │
    ▼
ChromaDB
    │
    ▼
Relevant Context
    │
    ▼
Llama 3.2
    │
    ▼
Answer
```

---

## API

### Upload tài liệu

```http
POST /upload
```

### Hỏi đáp

```http
POST /chat
```

Request:

```json
{
  "question": "Tóm tắt nội dung tài liệu"
}
```

Response:

```json
{
  "question": "...",
  "answer": "...",
  "sources": [...]
}
```

### Danh sách tài liệu

```http
GET /documents
```

### Xóa dữ liệu

```http
DELETE /documents
```

---

## Demo

1. Upload PDF hoặc TXT
2. Hệ thống đọc và index tài liệu
3. Người dùng đặt câu hỏi
4. Retriever tìm nội dung liên quan trong ChromaDB
5. Llama 3.2 sinh câu trả lời dựa trên tài liệu
6. Hiển thị nguồn tham khảo

---
## License

![License](https://img.shields.io/badge/License-MIT-yellow)

This project is licensed under the MIT License.