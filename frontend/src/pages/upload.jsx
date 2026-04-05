import { useState, useRef } from "react";

const API = "http://localhost:8000";

export default function Upload({ token, onUpload }) {
  const [dragging, setDragging]   = useState(false);
  const [file, setFile]           = useState(null);
  const [loading, setLoading]     = useState(false);
  const [error, setError]         = useState("");
  const [success, setSuccess]     = useState("");
  const inputRef                  = useRef();

  const handleFile = (f) => {
    setError("");
    setSuccess("");
    setFile(f);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);  // key name must match your FastAPI param

      const res = await fetch(`${API}/upload-docs`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,  // JWT auth
        },
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Upload failed");
        return;
      }

      setSuccess(`"${file.name}" uploaded successfully!`);
      setTimeout(() => onUpload(file.name), 1000); // go to chat after 1s
    } catch (err) {
      setError("Upload failed. Is the server running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: 520 }}>
      <h1>Upload Document</h1>
      <p className="subtitle">PDF, TXT, DOCX — anything your RAG backend supports</p>

      {error   && <div className="msg error">{error}</div>}
      {success && <div className="msg success">{success}</div>}

      {/* Drop Zone */}
      <div
        className={`dropzone ${dragging ? "active" : ""}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <div className="drop-icon">📄</div>
        {file ? (
          <p><strong>{file.name}</strong><br />{(file.size / 1024).toFixed(1)} KB</p>
        ) : (
          <p><strong>Click to browse</strong> or drag & drop your file here</p>
        )}
        {/* Hidden native file input */}
        <input
          ref={inputRef}
          type="file"
          style={{ display: "none" }}
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      <button
        className="btn btn-primary"
        style={{ marginTop: "1.2rem" }}
        onClick={handleUpload}
        disabled={!file || loading}
      >
        {loading ? "Uploading..." : "Upload & Continue →"}
      </button>
    </div>
  );
}
