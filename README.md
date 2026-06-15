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

## Tính năng

- Upload tài liệu PDF và TXT
- Tự động tạo vector embedding
- Lưu vector bằng ChromaDB
- Hỏi đáp dựa trên nội dung tài liệu
- Hiển thị nguồn tham khảo
- Lưu lịch sử chat trên trình duyệt
- Giao diện React + Bootstrap
- Backend FastAPI
- LLM chạy local bằng Ollama

---

## Công nghệ sử dụng

### Frontend

- React
- Vite
- Bootstrap 5
- Axios

### Backend

- FastAPI
- Uvicorn

### AI & RAG

- LlamaIndex
- ChromaDB
- Ollama
- Llama 3.2
- nomic-embed-text

### Xử lý tài liệu

- pdfplumber
- RapidOCR (fallback OCR)

---

## Kiến trúc hệ thống

```text
User
 │
 ▼
Frontend (React + Bootstrap)
 │
 ▼
FastAPI
 │
 ├── Upload Document
 │
 ├── LlamaIndex
 │
 ├── ChromaDB
 │
 └── Ollama
      ├── nomic-embed-text
      └── llama3.2
```

---

## Cấu trúc thư mục

```text
smart_doc_rag_web
│
├── backend
│   ├── app.py
│   ├── config.py
│   │
│   ├── routes
│   │   ├── upload.py
│   │   ├── chat.py
│   │   └── documents.py
│   │
│   └── services
│       ├── document_service.py
│       └── rag_service.py
│
├── frontend
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