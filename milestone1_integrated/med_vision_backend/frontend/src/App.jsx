import { useState } from "react";
import Auth from "./components/Auth";
import UploadDashboard from "./components/UploadDashboard";
import Viewer from "./components/Viewer";
import PredictionHistory from "./components/PredictionHistory";

export default function App() {
  const [token, setToken] = useState(localStorage.getItem("medvision_token"));
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [refreshCount, setRefreshCount] = useState(0);

  const handleLogout = () => {
    localStorage.removeItem("medvision_token");
    setToken(null);
    setSelectedRecord(null);
  };

  const handleJobFinished = (record) => {
    setSelectedRecord(record);
    setRefreshCount((c) => c + 1);
  };

  if (!token) {
    return (
      <Auth
        onLoginSuccess={() => setToken(localStorage.getItem("medvision_token"))}
      />
    );
  }

  return (
    <div
      style={{
        maxWidth: 960,
        margin: "30px auto",
        padding: "0 16px",
        fontFamily: "sans-serif",
      }}
    >
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 24,
        }}
      >
        <h2>MedVision Clinical Console</h2>
        <button
          onClick={handleLogout}
          style={{ padding: "6px 12px", cursor: "pointer" }}
        >
          Log Out
        </button>
      </header>
      <UploadDashboard onCompleted={handleJobFinished} />
      <Viewer prediction={selectedRecord} />
      <PredictionHistory
        onSelect={setSelectedRecord}
        refreshTrigger={refreshCount}
      />
    </div>
  );
}
