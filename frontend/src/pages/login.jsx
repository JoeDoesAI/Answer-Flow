import { useState } from "react";

// 🔌 CONNECT TO YOUR FASTAPI BACKEND
const API = "http://localhost:8000";

export default function Login({ onAuth, onGoRegister }) {
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  const handleLogin = async () => {
    setError("");
    setLoading(true);

    try {
      // FastAPI's OAuth2 login expects form data, not JSON
      const formData = new URLSearchParams();
      formData.append("username", email);  // FastAPI uses "username" by default
      formData.append("password", password);

      const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Login failed");
        return;
      }

      // data.access_token is the JWT from FastAPI
      onAuth(data.access_token);
    } catch (err) {
      setError("Could not reach server. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1>Welcome back</h1>
      <p className="subtitle">Sign in to your RAG workspace</p>

      {error && <div className="msg error">{error}</div>}

      <div className="field">
        <label>Email</label>
        <input
          type="email"
          placeholder="you@example.com"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="field">
        <label>Password</label>
        <input
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleLogin()}
        />
      </div>

      <button className="btn btn-primary" onClick={handleLogin} disabled={loading}>
        {loading ? "Signing in..." : "Sign In"}
      </button>

      <div className="link-text">
        No account? <span onClick={onGoRegister}>Register here</span>
      </div>
    </div>
  );
}
