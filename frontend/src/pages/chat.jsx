import { useState, useRef, useEffect } from "react";

const API = "http://localhost:8000";

export default function Chat({ token, filename, onNewUpload }) {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: `Document loaded: "${filename}". Ask me anything about it.`,
    },
  ]);
  const [input, setInput]     = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef             = useRef();

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    // Add user message to UI immediately
    const newMessages = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API}/query`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          query: text,
          filename: filename,   // send which doc to query against
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setMessages([...newMessages, {
          role: "assistant",
          content: `Error: ${data.detail || "Query failed"}`,
        }]);
        return;
      }

      // ⚠️ Adjust data.answer to match your FastAPI response field name
      setMessages([...newMessages, {
        role: "assistant",
        content: data.answer || data.response || JSON.stringify(data),
      }]);
    } catch (err) {
      setMessages([...newMessages, {
        role: "assistant",
        content: "Could not reach server. Is FastAPI running?",
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-layout">
      {/* Header */}
      <div className="chat-header">
        <h2>RAG Chat</h2>
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <span className="file-badge">📄 {filename}</span>
          <button
            className="btn btn-ghost"
            style={{ width: "auto", padding: "0.3rem 0.8rem", marginTop: 0, fontSize: "0.78rem" }}
            onClick={onNewUpload}
          >
            + New Doc
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
        {loading && (
          <div className="message assistant thinking">Thinking…</div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="chat-input-row">
        <input
          type="text"
          placeholder="Ask a question about your document…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="send-btn" onClick={sendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}
