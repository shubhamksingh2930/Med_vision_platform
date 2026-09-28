import { useState } from "react";
import { loginUser, registerUser } from "../api";

export default function Auth({ onLoginSuccess, onBack }) {
  const [isRegister, setIsRegister] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      if (isRegister) {
        await registerUser(email, password);
      }
      const data = await loginUser(email, password);
      localStorage.setItem("medvision_token", data.access_token);
      onLoginSuccess();
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    }
  };

  const inputStyle = {
    padding: 8,
    background: "var(--bg-card, #1a1a1a)",
    color: "var(--text-primary, #f0f0ee)",
    border: "0.5px solid var(--border, #2a2a2a)",
    borderRadius: 6,
    outline: "none",
    fontSize: 14,
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        background: "var(--bg, #0d0d0d)",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 400,
          padding: 24,
          background: "var(--bg-raised, #161616)",
          border: "0.5px solid var(--border, #2a2a2a)",
          borderRadius: 8,
        }}
      >
        <style>{`
          .auth-input::placeholder { color: var(--text-muted, #444444); opacity: 1; }
        `}</style>
        {onBack && (
          <a
            onClick={onBack}
            style={{
              fontSize: 12,
              color: "var(--text-muted, #444444)",
              textDecoration: "none",
              cursor: "pointer",
              marginBottom: "0.8rem",
              display: "block",
            }}
          >
            ← Back to home
          </a>
        )}
        <h3 style={{ color: "var(--text-primary, #f0f0ee)" }}>
          {isRegister ? "Create Account" : "Sign In to MedVision"}
        </h3>
        {error && (
          <p style={{ color: "var(--danger, #f87171)" }}>{error}</p>
        )}
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: 12 }}
        >
          <input
            className="auth-input"
            type="email"
            placeholder="Email address"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={inputStyle}
          />
          <input
            className="auth-input"
            type="password"
            placeholder="Password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={inputStyle}
          />
          <button
            type="submit"
            style={{
              padding: 10,
              cursor: "pointer",
              background: "var(--text-primary, #f0f0ee)",
              color: "var(--bg, #0d0d0d)",
              border: "none",
              borderRadius: 6,
              fontSize: 14,
              fontWeight: 500,
            }}
          >
            {isRegister ? "Register & Login" : "Log In"}
          </button>
        </form>
        <p
          style={{
            marginTop: 14,
            fontSize: 14,
            textAlign: "center",
            color: "var(--text-secondary, #888888)",
          }}
        >
          {isRegister ? "Already have an account?" : "Need an account?"}{" "}
          <button
            onClick={() => {
              setIsRegister(!isRegister);
              setError(null);
            }}
            style={{
              border: "none",
              background: "none",
              color: "var(--accent, #60a5fa)",
              cursor: "pointer",
              textDecoration: "none",
            }}
          >
            {isRegister ? "Sign In" : "Register"}
          </button>
        </p>
      </div>
    </div>
  );
}
