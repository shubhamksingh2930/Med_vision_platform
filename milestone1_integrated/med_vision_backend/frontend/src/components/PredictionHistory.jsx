import { useEffect, useState } from "react";
import { listPredictions, getPrediction } from "../api";

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
      <h4>Inference History</h4>
      {items.length === 0 ? (
        <p style={{ color: "#777" }}>No previous inferences found.</p>
      ) : (
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            textAlign: "left",
          }}
        >
          <thead>
            <tr style={{ borderBottom: "1px solid #ccc" }}>
              <th style={{ padding: 8 }}>ID</th>
              <th style={{ padding: 8 }}>Status</th>
              <th style={{ padding: 8 }}>Date</th>
              <th style={{ padding: 8 }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {items.map((item) => (
              <tr key={item.id} style={{ borderBottom: "1px solid #eee" }}>
                <td style={{ padding: 8 }}>{item.id.slice(0, 8)}...</td>
                <td style={{ padding: 8 }}>{item.status}</td>
                <td style={{ padding: 8 }}>
                  {new Date(item.created_at).toLocaleString()}
                </td>
                <td style={{ padding: 8 }}>
                  <button
                    onClick={async () => {
                      const { data } = await getPrediction(item.id);
                      onSelect(data);
                    }}
                    style={{ cursor: "pointer" }}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <div style={{ marginTop: 12, display: "flex", gap: 8 }}>
        <button disabled={page === 1} onClick={() => setPage((p) => p - 1)}>
          Prev
        </button>
        <span>
          Page {page} of {Math.max(1, Math.ceil(total / 10))}
        </span>
        <button
          disabled={page * 10 >= total}
          onClick={() => setPage((p) => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
