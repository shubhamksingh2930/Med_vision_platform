import { useEffect, useState } from "react";
import { listPredictions, getPrediction } from "../api";

const btnStyle = {
  cursor: "pointer",
  background: "var(--bg-card, #1a1a1a)",
  color: "var(--text-primary, #f0f0ee)",
  border: "0.5px solid var(--border, #2a2a2a)",
  borderRadius: 6,
  padding: "6px 12px",
  fontSize: 13,
};

export default function PredictionHistory({ onSelect, refreshTrigger }) {
  const [items, setItems] = useState([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);

  const fetchList = () => {
    listPredictions(page)
      .then(({ data }) => {
        setItems(data.items);
        setTotal(data.total);
      })
      .catch(console.error);
  };

  useEffect(() => {
    fetchList();
  }, [page, refreshTrigger]);

  return (
    <div style={{ marginTop: 32 }}>
      <h4 style={{ color: "var(--text-primary, #f0f0ee)" }}>Inference History</h4>
      {items.length === 0 ? (
        <p style={{ color: "var(--text-muted, #444444)" }}>No previous inferences found.</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            textAlign: "left",
          }}
        >
          <thead>
            <tr style={{ borderBottom: "1px solid var(--border, #2a2a2a)" }}>
              <th style={{ padding: 8, color: "var(--text-muted, #444444)", fontWeight: 500 }}>ID</th>
              <th style={{ padding: 8, color: "var(--text-muted, #444444)", fontWeight: 500 }}>Status</th>
              <th style={{ padding: 8, color: "var(--text-muted, #444444)", fontWeight: 500 }}>Date</th>
              <th style={{ padding: 8, color: "var(--text-muted, #444444)", fontWeight: 500 }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} style={{ borderBottom: "1px solid var(--border, #2a2a2a)" }}>
                <td style={{ padding: 8, color: "var(--text-secondary, #888888)" }}>{item.id.slice(0, 8)}...</td>
                <td style={{ padding: 8, color: "var(--text-secondary, #888888)" }}>{item.status}</td>
                <td style={{ padding: 8, color: "var(--text-secondary, #888888)" }}>
                  {new Date(item.created_at).toLocaleString()}
                </td>
                <td style={{ padding: 8 }}>
                  <button
                    onClick={async () => {
                      const { data } = await getPrediction(item.id);
                      onSelect(data);
                    }}
                    style={btnStyle}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div style={{ marginTop: 12, display: "flex", gap: 8, alignItems: "center" }}>
        <button disabled={page === 1} onClick={() => setPage((p) => p - 1)} style={btnStyle}>
          Prev
        </button>
        <span style={{ color: "var(--text-muted, #444444)", fontSize: 13 }}>
          Page {page} of {Math.max(1, Math.ceil(total / 10))}
        </span>
        <button
          disabled={page * 10 >= total}
          onClick={() => setPage((p) => p + 1)}
          style={btnStyle}
        >
          Next
        </button>
      </div>
    </div>
  );
}
