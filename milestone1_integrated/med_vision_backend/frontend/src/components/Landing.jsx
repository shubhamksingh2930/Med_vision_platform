import { useRef } from "react";

const c = {
  textPrimary: "var(--text-primary, #f0f0ee)",
  textSecondary: "var(--text-secondary, #888888)",
  textMuted: "var(--text-muted, #444444)",
  textAccent: "var(--accent, #60a5fa)",
  textDanger: "var(--danger, #f87171)",
  surface1: "var(--bg-raised, #161616)",
  surface2: "var(--bg, #0d0d0d)",
  bgAccent: "var(--accent-bg, #1e3a5f)",
  border: "var(--border, #2a2a2a)",
  borderStrong: "var(--border-strong, #333333)",
  radius: "var(--radius, 8px)",
  fontSans: "var(--font-sans, system-ui, -apple-system, sans-serif)",
};

const primaryButton = {
  background: c.textPrimary,
  color: c.surface2,
  padding: "13px 20px",
  borderRadius: 8,
  fontSize: 14,
  fontWeight: 500,
  border: "none",
  cursor: "pointer",
  fontFamily: c.fontSans,
};

const textButton = {
  background: "none",
  border: "none",
  padding: 0,
  fontSize: 13,
  color: c.textMuted,
  cursor: "pointer",
  fontFamily: c.fontSans,
};

const findings = [
  { label: "Effusion", value: 78, fill: c.textDanger },
  { label: "Cardiomegaly", value: 42, fill: c.borderStrong },
  { label: "Atelectasis", value: 31, fill: c.borderStrong },
  { label: "Pneumonia", value: 12, fill: c.borderStrong },
];

const versus = [
  {
    ai: "A paragraph that sounds confident but can't show its work",
    mv: "18 probabilities, one heatmap, one region highlighted",
  },
  {
    ai: "Single diagnosis, no uncertainty",
    mv: "Multiple findings can fire simultaneously — the way real films present",
  },
];

const stats = [
  { value: "18", label: "pathological findings scored" },
  { value: "1", label: "X-ray in, full report out" },
  { value: "∞", label: "free to use" },
];

const responsiveCss = `
.lp-nav-inner { padding: 1rem 1.5rem; }
.lp-top { display: flex; flex-direction: column; }
.lp-hero { padding: 2.8rem 1.5rem 0; }
.lp-h1 { font-size: 28px; }
.lp-sub { font-size: 14px; max-width: 300px; }
.lp-demo {
  display: flex;
  gap: 1rem;
  padding: 1.2rem 1.5rem;
  background: var(--bg-raised, #161616);
  border-top: 1px solid var(--border, #2a2a2a);
  border-bottom: 1px solid var(--border, #2a2a2a);
}
.lp-track { height: 3px; }
.lp-body { padding: 2rem 1.5rem; }
.lp-quote { font-size: 16px; }
.lp-stat-num { font-size: 22px; }
.lp-bar { padding: 1rem 1.5rem; border-top: 1px solid var(--border, #2a2a2a); }
@media (min-width: 768px) {
  .lp-nav-inner { padding: 1rem 2.5rem; }
  .lp-top {
    flex-direction: row;
    align-items: center;
    gap: 3rem;
    max-width: 1100px;
    margin: 0 auto;
    padding: 4rem 2.5rem;
    box-sizing: border-box;
  }
  .lp-hero { flex: 55 1 0; padding: 0; }
  .lp-h1 { font-size: 42px; }
  .lp-sub { font-size: 16px; max-width: 420px; }
  .lp-demo-wrap { flex: 45 1 0; min-width: 0; }
  .lp-demo {
    flex-direction: row;
    align-items: flex-start;
    gap: 1rem;
    width: 100%;
    box-sizing: border-box;
    padding: 1.5rem;
    background: var(--bg-raised, #161616);
    border: 0.5px solid var(--border, #2a2a2a);
    border-radius: 12px;
  }
  .lp-track { height: 5px; }
  .lp-body { padding: 2rem 2.5rem; }
  .lp-quote { font-size: 20px; }
  .lp-stat-num { font-size: 32px; }
  .lp-bar {
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    width: 100%;
    box-sizing: border-box;
    border-radius: 12px 12px 0 0;
    border-left: 0.5px solid var(--border, #2a2a2a);
    border-right: 0.5px solid var(--border, #2a2a2a);
  }
}
`;

const tagBase = {
  fontSize: 11,
  padding: "2px 8px",
  borderRadius: 10,
  whiteSpace: "nowrap",
  flexShrink: 0,
  lineHeight: 1.5,
};

function Tag({ kind }) {
  const isAi = kind === "ai";
  return (
    <span
      style={{
        ...tagBase,
        background: isAi ? "var(--bg-card, #1a1a1a)" : c.bgAccent,
        color: isAi ? c.textMuted : c.textAccent,
        border: `0.5px solid ${isAi ? c.border : "transparent"}`,
      }}
    >
      {isAi ? "AI chat" : "MedViss"}
    </span>
  );
}

function VersusRow({ kind, text }) {
  return (
    <div
      style={{
        display: "flex",
        gap: 8,
        alignItems: "flex-start",
        marginBottom: 8,
      }}
    >
      <Tag kind={kind} />
      <span
        style={{
          fontSize: 13,
          lineHeight: 1.5,
          color: kind === "ai" ? c.textSecondary : c.textPrimary,
        }}
      >
        {text}
      </span>
    </div>
  );
}

export default function Landing({ onSignIn }) {
  const demoRef = useRef(null);

  const scrollToDemo = () => {
    demoRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  };

  return (
    <div
      style={{
        width: "100%",
        minHeight: "100vh",
        display: "flex",
        flexDirection: "column",
        fontFamily: c.fontSans,
        color: c.textPrimary,
        background: c.surface2,
      }}
    >
      <style>{responsiveCss}</style>
      <nav style={{ borderBottom: `1px solid ${c.border}` }}>
        <div
          className="lp-nav-inner"
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            maxWidth: 1200,
            margin: "0 auto",
          }}
        >
          <span
            style={{ fontSize: 16, fontWeight: 500, letterSpacing: "-0.02em" }}
          >
            Med<span style={{ color: c.textAccent }}>viss</span>
          </span>
          <button
            onClick={onSignIn}
            style={{ ...textButton, color: c.textPrimary }}
          >
            Sign in
          </button>
        </div>
      </nav>

      <div className="lp-top">
        <section className="lp-hero">
          <div
            style={{
              fontSize: 11,
              letterSpacing: "0.08em",
              color: c.textMuted,
              marginBottom: "0.8rem",
            }}
          >
            CHEST X-RAY ANALYSIS
          </div>
          <h1
            className="lp-h1"
            style={{
              fontWeight: 500,
              letterSpacing: "-0.03em",
              lineHeight: 1.25,
              margin: "0 0 1rem",
              color: c.textPrimary,
            }}
          >
            What did the model{" "}
            <em
              style={{
                fontStyle: "italic",
                color: c.textSecondary,
                fontWeight: 400,
              }}
            >
              actually
            </em>{" "}
            look at?
          </h1>
          <p
            className="lp-sub"
            style={{
              color: c.textSecondary,
              lineHeight: 1.65,
              margin: "0 0 1.6rem",
            }}
          >
            Upload a chest X-ray. Get probability scores across 18 pathological
            findings — with a heatmap showing the exact region that drove each
            result.
          </p>
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 8,
              marginBottom: "2rem",
            }}
          >
            <button onClick={onSignIn} style={primaryButton}>
              Upload your first X-ray →
            </button>
            <button
              onClick={scrollToDemo}
              style={{ ...textButton, padding: "8px 0" }}
            >
              See a real prediction ↓
            </button>
          </div>
        </section>

        <div className="lp-demo-wrap">
          <section ref={demoRef} className="lp-demo">
            <div
              className="lp-xray"
              style={{
                position: "relative",
                width: 72,
                height: 88,
                flexShrink: 0,
                background: "#080808",
                borderRadius: 6,
                overflow: "hidden",
              }}
            >
              <svg
                width="72"
                height="88"
                viewBox="0 0 72 88"
                style={{ display: "block" }}
              >
                <ellipse
                  cx="36"
                  cy="46"
                  rx="30"
                  ry="38"
                  fill="none"
                  stroke="#2a2a2a"
                  strokeWidth="1.5"
                />
                <ellipse
                  cx="23"
                  cy="42"
                  rx="11"
                  ry="22"
                  fill="#333"
                  opacity="0.55"
                />
                <ellipse
                  cx="49"
                  cy="42"
                  rx="11"
                  ry="22"
                  fill="#333"
                  opacity="0.55"
                />
                <rect
                  x="34"
                  y="14"
                  width="4"
                  height="62"
                  rx="2"
                  fill="#2d2d2d"
                />
              </svg>
              <div
                style={{
                  position: "absolute",
                  top: 18,
                  left: 12,
                  width: 36,
                  height: 32,
                  background:
                    "radial-gradient(ellipse, rgba(239,68,68,0.6) 0%, rgba(251,146,60,0.3) 50%, transparent 75%)",
                }}
              />
            </div>

            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontSize: 11, color: c.textMuted }}>
                PA_chest_0042.jpg
              </div>
              <div
                style={{
                  fontSize: 18,
                  fontWeight: 500,
                  color: c.textDanger,
                  letterSpacing: "-0.02em",
                  marginTop: 2,
                }}
              >
                Effusion
              </div>
              <div
                style={{
                  fontSize: 13,
                  color: c.textSecondary,
                  marginBottom: 8,
                }}
              >
                78% probability
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {findings.map((f) => (
                  <div
                    key={f.label}
                    style={{ display: "flex", alignItems: "center", gap: 6 }}
                  >
                    <span
                      style={{
                        fontSize: 11,
                        color: c.textMuted,
                        width: 72,
                        flexShrink: 0,
                      }}
                    >
                      {f.label}
                    </span>
                    <div
                      className="lp-track"
                      style={{
                        flex: 1,
                        borderRadius: 2,
                        background: c.border,
                        overflow: "hidden",
                      }}
                    >
                      <div
                        style={{
                          width: `${f.value}%`,
                          height: "100%",
                          background: f.fill,
                        }}
                      />
                    </div>
                    <span
                      style={{
                        fontSize: 10,
                        color: c.textMuted,
                        minWidth: 24,
                        textAlign: "right",
                      }}
                    >
                      {f.value}%
                    </span>
                  </div>
                ))}
              </div>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 4,
                  marginTop: 8,
                  fontSize: 11,
                  color: c.textMuted,
                }}
              >
                <svg
                  width="12"
                  height="12"
                  viewBox="0 0 16 16"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="1.3"
                >
                  <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" />
                  <circle cx="8" cy="8" r="2" />
                </svg>
                Grad-CAM heatmap generated
              </div>
            </div>
          </section>
        </div>
      </div>

      <section
        className="lp-body"
        style={{
          maxWidth: 800,
          margin: "0 auto",
          width: "100%",
          boxSizing: "border-box",
        }}
      >
        <blockquote
          className="lp-quote"
          style={{
            margin: "0 0 2rem",
            borderLeft: `2px solid ${c.borderStrong}`,
            paddingLeft: "1rem",
            color: c.textSecondary,
            lineHeight: 1.6,
            letterSpacing: "-0.01em",
          }}
        >
          ChatGPT says{" "}
          <strong style={{ color: c.textPrimary, fontWeight: 500 }}>
            "possible signs of pneumonia."
          </strong>{" "}
          That's an opinion. This shows you the{" "}
          <span style={{ color: c.textAccent }}>pixel-level evidence</span>.
        </blockquote>

        <div style={{ marginBottom: "2rem" }}>
          <div
            style={{
              fontSize: 11,
              color: c.textMuted,
              letterSpacing: "0.06em",
              marginBottom: "0.8rem",
            }}
          >
            THE DIFFERENCE
          </div>
          {versus.map((row) => (
            <div key={row.ai} style={{ marginBottom: 8 }}>
              <VersusRow kind="ai" text={row.ai} />
              <VersusRow kind="mv" text={row.mv} />
            </div>
          ))}
        </div>

        <div
          style={{
            display: "flex",
            gap: 1,
            background: c.border,
            border: `1px solid ${c.border}`,
            borderRadius: 10,
            overflow: "hidden",
            marginBottom: "2rem",
          }}
        >
          {stats.map((s) => (
            <div
              key={s.label}
              style={{
                flex: 1,
                background: c.surface1,
                textAlign: "center",
                padding: "0.9rem 0.8rem",
              }}
            >
              <div
                className="lp-stat-num"
                style={{
                  fontWeight: 500,
                  letterSpacing: "-0.03em",
                  color: c.textPrimary,
                }}
              >
                {s.value}
              </div>
              <div
                style={{
                  fontSize: 10,
                  color: c.textMuted,
                  marginTop: 2,
                  lineHeight: 1.4,
                }}
              >
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      <footer
        style={{
          padding: "1rem 1.5rem 2rem",
          borderTop: `1px solid ${c.border}`,
          fontSize: 12,
          color: c.textMuted,
          lineHeight: 1.6,
        }}
      >
        Built for NEET-PG prep and radiology learners. The model uses pretrained
        weights from torchxrayvision — not clinically validated, not a
        substitute for a radiologist's read.
      </footer>

      <div
        className="lp-bar"
        style={{
          position: "sticky",
          bottom: 0,
          marginTop: "auto",
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: c.surface2,
        }}
      >
        <button onClick={onSignIn} style={{ ...primaryButton, flex: 1 }}>
          Get started free
        </button>
        <button onClick={onSignIn} style={textButton}>
          Already have an account?
        </button>
      </div>
    </div>
  );
}
