import { useState, useEffect } from "react";
import Auth from "./components/Auth";
import Landing from "./components/Landing";
import UploadDashboard from "./components/UploadDashboard";
import Viewer from "./components/Viewer";
import PredictionHistory from "./components/PredictionHistory";

const getExpiry = () => {
  const token = localStorage.getItem('medvision_token');
  if (!token) return null;
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const remaining = payload.exp * 1000 - Date.now();
    if (remaining <= 0) return null;
    const hours = Math.floor(remaining / 3600000);
    const mins = Math.floor((remaining % 3600000) / 60000);
    return { label: hours > 0 ? `${hours}h ${mins}m` : `${mins}m`, warning: remaining < 900000 };
  } catch { return null; }
};

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("medvision_token"));
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [refreshCount, setRefreshCount] = useState(0);
  const [showAuth, setShowAuth] = useState(false);
  const [expiry, setExpiry] = useState(getExpiry);

  useEffect(() => {
    const id = setInterval(() => setExpiry(getExpiry()), 60000);
    return () => clearInterval(id);
  }, []);

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
        onLoginSuccess={() => {
          setToken(localStorage.getItem("medvision_token"));
          setExpiry(getExpiry());
        }}
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
        <div style={{ display: "flex", alignItems: "center" }}>
          {expiry && (
            <span style={{
              fontSize: '11px',
              color: expiry.warning
                ? 'var(--danger, #f87171)'
                : 'var(--text-muted, #444444)',
              marginRight: '12px'
            }}>
              Session {expiry.label}
            </span>
          )}
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
        </div>
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
