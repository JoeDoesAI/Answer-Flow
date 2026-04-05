import { useState } from "react";

const API = "http://localhost:8000";

export default function Register({ onAuth, onGoLogin }) {
  const [email, setEmail]       = useState("");
  const [password, setPassword] = useState("");
  const [firstname, setFirstName] = useState("");
  const [lastname, setLastName] = useState("");
  const [error, setError]       = useState("");
  const [loading, setLoading]   = useState(false);

  const handleRegister = async () => {
    setError("");
    setLoading(true);

    try {
      const res = await fetch(`${API}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ firstname,lastname, email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Registration failed");
        return;
      }

      // After registering, log them in automatically
      const formData = new URLSearchParams();
      formData.append("email", email);
      formData.append("password", password);

      const loginRes = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      const loginData = await loginRes.json();
      if (!loginRes.ok) {
        setError("Registered! But auto-login failed — please sign in.");
        return;
      }

      onAuth(loginData.access_token);
    } catch (err) {
      setError("Could not reach server. Is FastAPI running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h1>Create account</h1>
      <p className="subtitle">Start chatting with your documents</p>

      {error && <div className="msg error">{error}</div>}

      <div className="field">
        <label>First Name</label>
        <input
          type="text"
          placeholder="Enter your first name"
          value={firstname}
          onChange={(e) => setFirstName(e.target.value)}
        />
      </div>

       <div className="field">
        <label>Last Name</label>
        <input
          type="text"
          placeholder="Enter your last name"
          value={lastname}
          onChange={(e) => setLastName(e.target.value)}
        />
      </div>

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
          placeholder="Create a password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleRegister()}
        />
      </div>

      <button className="btn btn-primary" onClick={handleRegister} disabled={loading}>
        {loading ? "Creating account..." : "Create Account"}
      </button>

      <div className="link-text">
        Already have an account? <span onClick={onGoLogin}>Sign in</span>
      </div>
    </div>
  );
}
