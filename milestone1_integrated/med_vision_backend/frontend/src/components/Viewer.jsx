export default function Viewer({ prediction }) {
  if (!prediction) return null;

  const sigmoid = (z) => 1 / (1 + Math.exp(-z));

  let findings = [];
  if (prediction.prediction_result) {
    try {
      const raw =
        typeof prediction.prediction_result === "string"
          ? JSON.parse(prediction.prediction_result)
          : prediction.prediction_result;

      findings = Object.entries(raw)
        .map(([pathology, val]) => {
          const prob = val >= 0 && val <= 1 ? val : sigmoid(val);
          return [pathology, prob];
        })
        .sort((a, b) => b[1] - a[1]);
    } catch (e) {
      console.error("Failed to parse prediction result", e);
    }
  }

  return (
    <div
      style={{
        marginTop: 24,
        padding: 20,
        background: "var(--bg-raised, #161616)",
        border: "0.5px solid var(--border, #2a2a2a)",
        borderRadius: 8,
      }}
    >
      <h3 style={{ color: "var(--text-primary, #f0f0ee)" }}>
        Prediction #{prediction.id.slice(0, 8)}
      </h3>
      <div style={{ display: "flex", gap: 24, flexWrap: "wrap" }}>
        <div>
          <h4 style={{ color: "var(--text-secondary, #888888)" }}>Input X-Ray</h4>
          {prediction.original_image_url ? (
            <img
              src={prediction.original_image_url}
              alt="Original X-Ray"
              width={300}
              style={{ borderRadius: 4, display: "block", border: "1px solid var(--border, #2a2a2a)" }}
            />
          ) : (
            <p style={{ color: "var(--text-muted, #444444)" }}>No original image URL</p>
          )}
        </div>
        <div>
          <h4 style={{ color: "var(--text-secondary, #888888)" }}>GradCAM Explanation</h4>
          {prediction.heatmap_image_url ? (
            <img
              src={prediction.heatmap_image_url}
              alt="Heatmap"
              width={300}
              style={{ borderRadius: 4, display: "block", border: "1px solid var(--border, #2a2a2a)" }}
            />
          ) : (
            <p style={{ color: "var(--text-muted, #444444)" }}>No heatmap available</p>
          )}
        </div>
        <div style={{ flex: 1, minWidth: 220 }}>
          <h4 style={{ color: "var(--text-secondary, #888888)" }}>Model Findings</h4>
          {findings.length > 0 ? (
            <ul style={{ listStyle: "none", padding: 0 }}>
              {findings.map(([pathology, prob]) => (
                <li
                  key={pathology}
                  style={{
                    margin: "6px 0",
                    display: "flex",
                    justifyContent: "space-between",
                    color: "var(--text-primary, #f0f0ee)",
                  }}
                >
                  <span>{pathology}</span>
                  <strong style={{ color: "var(--text-secondary, #888888)" }}>
                    {(prob * 100).toFixed(1)}%
                  </strong>
                </li>
              ))}
            </ul>
          ) : (
            <p style={{ color: "var(--text-muted, #444444)" }}>No findings recorded.</p>
          )}
        </div>
      </div>
    </div>
  );
}
