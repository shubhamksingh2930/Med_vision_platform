import { useState } from "react";
import { createPrediction, subscribeToEvents, getPrediction } from "../api";

export default function UploadDashboard({ onCompleted }) {
  const [status, setStatus] = useState("idle");
  const [errorMessage, setErrorMessage] = useState(null);

  const handleFile = async (file) => {
    if (!file) return;
    setStatus("uploading");
    setErrorMessage(null);

    try {
      const { data } = await createPrediction(file);
      setStatus(data.status);

      const sse = subscribeToEvents(data.id, async ({ status: newStatus }) => {
        setStatus(newStatus);
        if (newStatus === "completed") {
          sse.close();
          const { data: fullRecord } = await getPrediction(data.id);
          onCompleted(fullRecord);
        } else if (newStatus === "failed") {
          sse.close();
          setErrorMessage("Processing failed. Please check worker logs.");
        }
      });
    } catch (err) {
      setStatus("idle");
      setErrorMessage(err.response?.data?.detail || "Upload failed");
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div>
      <div
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        onClick={() => document.getElementById("fileInput").click()}
        style={{
          border: "2px dashed #888",
          borderRadius: 8,
          padding: 36,
          textAlign: "center",
          cursor: "pointer",
          backgroundColor: "#fafafa",
        }}
      >
        <input
          id="fileInput"
          type="file"
          accept="image/png,image/jpeg"
          hidden
          onChange={(e) => handleFile(e.target.files[0])}
        />
        <p style={{ margin: 0, fontWeight: "bold" }}>
          Drop chest X-ray here (PNG / JPEG), or click to upload
        </p>
        <p style={{ margin: "8px 0 0", color: "#555" }}>Status: {status}</p>
      </div>
      {errorMessage && (
        <p style={{ color: "red", marginTop: 8 }}>{errorMessage}</p>
      )}
    </div>
  );
}
