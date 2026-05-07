import { useState } from "react";
import Login from "./pages/login";
import Register from "./pages/register";
import Upload from "./pages/upload";
import "./index.css";

export default function App() {
  const [page, setPage] = useState("login"); // "login" | "register" | "upload" | "chat"
  const [token, setToken] = useState(null);  // JWT from FastAPI
  const [uploadedFile, setUploadedFile] = useState(null);

  // Called after successful login/register
  const handleAuth = (jwt) => {
    setToken(jwt);
    setPage("upload");
  };

  // Called after successful upload
  const handleUpload = (filename) => {
    setUploadedFile(filename);
    setPage("chat");
  };

  return (
    <div className="app">
      {page === "login" && (
        <Login onAuth={handleAuth} onGoRegister={() => setPage("register")} />
      )}
      {page === "register" && (
        <Register onAuth={handleAuth} onGoLogin={() => setPage("login")} />
      )}
      {page === "upload" && (
        <Upload token={token} onUpload={handleUpload} />
      )}
      {page === "chat" && (
        <Chat token={token} filename={uploadedFile} onNewUpload={() => setPage("upload")} />
      )}
    </div>
  );
}
