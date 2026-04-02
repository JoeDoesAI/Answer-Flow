import { useState } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Upload from "./pages/Upload";
import Chat from "./pages/Chat";
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
