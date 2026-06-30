import { useEffect, useRef, useState } from "react";
import {
  uploadDocument,
  askQuestion,
  getDocuments,
  deleteDocuments,
} from "./api";

function normalizeForMatch(text = "") {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function isNoAnswerContent(text = "") {
  const normalized = normalizeForMatch(text);

  return (
    normalized.includes("khong tim thay") ||
    normalized.includes("toi khong tim thay") ||
    normalized.includes("khong co thong tin") ||
    normalized.includes("khong du thong tin")
  );
}

function SourceCitations({ sources, answer }) {
  if (!sources || sources.length === 0 || isNoAnswerContent(answer)) {
    return null;
  }

  return (
    <details className="source-citations mt-3">
      <summary>
        <i className="bi bi-link-45deg me-1"></i>
        Nguồn tham khảo ({sources.length})
      </summary>

      <div className="source-list">
        {sources.map((source, sourceIndex) => {
          const index = source.index || sourceIndex + 1;
          const fileName = source.file_name || `Nguồn ${index}`;
          const pageLabel = source.page ? `Trang ${source.page}` : "Đoạn liên quan";

          return (
            <div className="source-box" key={`${fileName}-${pageLabel}-${index}`}>
              <div className="source-meta">
                <span className="source-index">[{index}]</span>
                <span className="source-title" title={fileName}>{fileName}</span>
                <span className="source-page">{pageLabel}</span>
              </div>
              <div className="source-preview">{source.preview}</div>
            </div>
          );
        })}
      </div>
    </details>
  );
}

function SourceCitationsV2({ sources, answer }) {
  if (!sources || sources.length === 0 || isNoAnswerContent(answer)) {
    return null;
  }

  return (
    <details className="source-citations mt-3">
      <summary>
        <i className="bi bi-link-45deg me-1"></i>
        Nguồn tham khảo ({sources.length})
      </summary>

      <div className="source-list">
        {sources.map((source, sourceIndex) => {
          const index = source.index || sourceIndex + 1;
          const fileName = source.file_name || `Nguồn ${index}`;
          const pageLabel = source.page
            ? `Trang ${source.page}`
            : `Đoạn ${source.section || source.chunk_id || index}`;

          return (
            <div className="source-box" key={`${fileName}-${pageLabel}-${index}`}>
              <div className="source-meta">
                <span className="source-index">[{index}]</span>
                <span className="source-title" title={fileName}>{fileName}</span>
                <span className="source-page">{pageLabel}</span>
              </div>
              <div className="source-preview">{source.preview}</div>
            </div>
          );
        })}
      </div>
    </details>
  );
}

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem("chat_history");

    if (saved) {
      return JSON.parse(saved);
    }

    return [
      {
        role: "bot",
        content:
          "Xin chào! Hãy upload tài liệu PDF/TXT/DOCX bên trái, sau đó đặt câu hỏi về tài liệu.",
      },
    ];
  });
  useEffect(() => {
    localStorage.setItem("chat_history", JSON.stringify(messages));
  }, [messages]);

  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);
  const [status, setStatus] = useState("");
  const chatEndRef = useRef(null);

  async function loadDocuments() {
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (error) {
      console.error(error);
      setStatus("Không kết nối được backend. Hãy chạy FastAPI trước.");
    }
  }

  useEffect(() => {
    loadDocuments();
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleUpload() {
    if (!selectedFile) {
      setStatus("Vui lòng chọn file PDF hoặc TXT.");
      return;
    }

    setUploading(true);
    setStatus("Đang upload và index tài liệu...");

    try {
      const data = await uploadDocument(selectedFile);

      setStatus(`Upload thành công: ${data.filename}`);
      setSelectedFile(null);
      await loadDocuments();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          content: `Đã index tài liệu "${data.filename}" vào ChromaDB bằng LlamaIndex.`,
        },
      ]);
    } catch (error) {
      console.error(error);
      const detail =
        error.response?.data?.detail ||
        error.response?.data ||
        error.message ||
        "Upload thất bại";
      setStatus(`Lỗi upload: ${JSON.stringify(detail)}`);
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk(e) {
  e.preventDefault();

  const cleanQuestion = question.trim();

  if (!cleanQuestion) return;

  // Tin nhắn user
  setMessages((prev) => [
    ...prev,
    {
      role: "user",
      content: cleanQuestion,
    },
  ]);

  setQuestion("");
  setAsking(true);

  try {
    const data = await askQuestion(cleanQuestion);

    setMessages((prev) => [
      ...prev,
      {
        role: "bot",
        content: data.answer || "Không có câu trả lời.",
        sources: data.sources || [],
      },
    ]);
  } catch (error) {
    console.error(error);

    const detail =
      error.response?.data?.detail ||
      error.response?.data ||
      error.message ||
      "Chat thất bại";

    setMessages((prev) => [
      ...prev,
      {
        role: "bot",
        content: `Lỗi: ${JSON.stringify(detail)}`,
      },
    ]);
  } finally {
    setAsking(false);
  }
}

  async function handleClear() {
    const ok = window.confirm("Xóa toàn bộ tài liệu và ChromaDB?");
    if (!ok) return;

    try {
      await deleteDocuments();
      await loadDocuments();
      localStorage.removeItem("chat_history");
      setMessages([
        {
          role: "bot",
          content: "Đã xóa tài liệu và vector database.",
        },
      ]);
      setStatus("Đã xóa dữ liệu.");
    } catch (error) {
      console.error(error);
      setStatus("Xóa thất bại.");
    }
  }

  return (
    <div className="min-vh-100 bg-light">
      <nav className="navbar navbar-dark bg-primary shadow-sm">
        <div className="container">
          <span className="navbar-brand fw-bold">
            Document RAG
          </span>
          <span className="badge text-bg-light">
            LlamaIndex + ChromaDB + Ollama
          </span>
        </div>
      </nav>

      <main className="container py-4">
        {status && (
          <div className="alert alert-info alert-dismissible fade show">
            {status}
            <button
              type="button"
              className="btn-close"
              onClick={() => setStatus("")}
            ></button>
          </div>
        )}

        <div className="row g-4">
          <div className="col-lg-4">
            <div className="card shadow-sm mb-4">
              <div className="card-header bg-white fw-bold">
                <i className="bi bi-file-earmark-arrow-up me-2"></i>
                Upload tài liệu
              </div>

              <div className="card-body">
                <input
                  className="form-control mb-3"
                  type="file"
                  accept=".pdf,.txt,.docx"
                  onChange={(e) => setSelectedFile(e.target.files[0])}
                />

                <button
                  className="btn btn-primary w-100"
                  onClick={handleUpload}
                  disabled={uploading}
                >
                  {uploading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Đang xử lý...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-cloud-upload me-2"></i>
                      Upload & Index
                    </>
                  )}
                </button>

                <div className="small text-muted mt-3">
                  Hỗ trợ PDF, DOCX và TXT. Khi upload, backend sẽ đọc tài liệu,
                  tạo embedding bằng Ollama và lưu vector vào ChromaDB.
                </div>
              </div>
            </div>

            <div className="card shadow-sm">
              <div className="card-header bg-white d-flex justify-content-between align-items-center">
                <span className="fw-bold">
                  <i className="bi bi-folder2-open me-2"></i>
                  Tài liệu
                </span>
                <button className="btn btn-sm btn-outline-secondary" onClick={loadDocuments}>
                  <i className="bi bi-arrow-clockwise"></i>
                </button>
              </div>

              <div className="card-body">
                {documents.length === 0 ? (
                  <div className="text-muted small">Chưa có tài liệu.</div>
                ) : (
                  <ul className="list-group mb-3">
                    {documents.map((doc) => (
                      <li
                        className="list-group-item d-flex justify-content-between align-items-center"
                        key={doc.path}
                      >
                        <span className="text-truncate">
                          <i className="bi bi-file-earmark-text me-2"></i>
                          {doc.filename}
                        </span>
                        <span className="badge text-bg-secondary">
                          {Math.round(doc.size / 1024)} KB
                        </span>
                      </li>
                    ))}
                  </ul>
                )}

                <button className="btn btn-outline-danger w-100" onClick={handleClear}>
                  <i className="bi bi-trash me-2"></i>
                  Xóa tài liệu + ChromaDB
                </button>
              </div>
            </div>
          </div>

          <div className="col-lg-8">
            <div className="card shadow-sm chat-card">
              <div className="card-header bg-white fw-bold">
                <i className="bi bi-chat-dots me-2"></i>
                Hỏi đáp tài liệu
              </div>

              <div className="card-body chat-box">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`message-row ${message.role === "user" ? "justify-content-end" : "justify-content-start"
                      }`}
                  >
                    <div
                      className={`message-bubble ${message.role === "user" ? "user-bubble" : "bot-bubble"
                        }`}
                    >
                      <div className="fw-bold mb-1">
                        {message.role === "user" ? "Bạn" : "Gelato"}
                      </div>
                      <div className="message-content">{message.content}
                        <SourceCitationsV2 sources={message.sources} answer={message.content} />
                      </div>
                    </div>
                  </div>
                ))}

                {asking && (
                  <div className="message-row justify-content-start">
                    <div className="message-bubble bot-bubble">
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Đang suy nghĩ...
                    </div>
                  </div>
                )}

                <div ref={chatEndRef}></div>
              </div>

              <div className="card-footer bg-white">
                <form onSubmit={handleAsk} className="d-flex gap-2">
                  <input
                    className="form-control"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    placeholder="Nhập câu hỏi về tài liệu..."
                    disabled={asking}
                  />
                  <button className="btn btn-success px-4" disabled={asking}>
                    <i className="bi bi-send"></i>
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
