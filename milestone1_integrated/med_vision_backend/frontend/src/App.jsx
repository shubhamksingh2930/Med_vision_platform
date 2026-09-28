import { useState } from "react";
import Auth from "./components/Auth";
import Landing from "./components/Landing";
import UploadDashboard from "./components/UploadDashboard";
import Viewer from "./components/Viewer";
import PredictionHistory from "./components/PredictionHistory";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("medvision_token"));
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [refreshCount, setRefreshCount] = useState(0);
  const [showAuth, setShowAuth] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("medvision_token");
    setToken(null);
    setSelectedRecord(null);
  };

  const handleJobFinished = (record) => {
    setSelectedRecord(record);
    setRefreshCount((c) => c + 1);
  };

  if (!token && !showAuth) {
    return <Landing onSignIn={() => setShowAuth(true)} />;
  }

  if (!token) {
    return (
      <Auth
        onLoginSuccess={() => setToken(localStorage.getItem("medvision_token"))}
        onBack={() => setShowAuth(false)}
      />
    );
  }

  return (
    <div
      style={{
        maxWidth: 960,
        margin: "0 auto",
        padding: "0 16px",
        fontFamily: "inherit",
      }}
    >
      <nav
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "1rem 1.5rem",
          marginLeft: "-16px",
          marginRight: "-16px",
          borderBottom: "0.5px solid var(--border, #2a2a2a)",
          background: "var(--bg, #0d0d0d)",
          marginBottom: 24,
        }}
      >
        <span
          style={{
            fontSize: 15,
            fontWeight: 500,
            letterSpacing: "-0.02em",
          }}
        >
          Med<span style={{ color: "var(--accent, #60a5fa)" }}>viss</span>
        </span>
        <button
          onClick={handleLogout}
          style={{
            background: "transparent",
            color: "var(--text-muted, #444444)",
            border: "0.5px solid var(--border, #2a2a2a)",
            padding: "6px 14px",
            borderRadius: 6,
            fontSize: 13,
            cursor: "pointer",
            fontFamily: "inherit",
          }}
        >
          Log Out
        </button>
      </nav>
      <UploadDashboard onCompleted={handleJobFinished} />
      <Viewer prediction={selectedRecord} />
      <PredictionHistory
        onSelect={setSelectedRecord}
        refreshTrigger={refreshCount}
      />
    </div>
  );
}
