import { useState } from "react";
import { loginUser, registerUser } from "../api";

export default function Auth({ onLoginSuccess }) {
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

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "60px auto",
        padding: 24,
        border: "1px solid #ddd",
        borderRadius: 8,
      }}
    >
      <h3>{isRegister ? "Create Account" : "Sign In to MedVision"}</h3>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form
        onSubmit={handleSubmit}
        style={{ display: "flex", flexDirection: "column", gap: 12 }}
      >
        <input
          type="email"
          placeholder="Email address"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{ padding: 8 }}
        />
        <input
          type="password"
          placeholder="Password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ padding: 8 }}
        />
        <button type="submit" style={{ padding: 10, cursor: "pointer" }}>
          {isRegister ? "Register & Login" : "Log In"}
        </button>
      </form>
      <p style={{ marginTop: 14, fontSize: 14, textAlign: "center" }}>
        {isRegister ? "Already have an account?" : "Need an account?"}{" "}
        <button
          onClick={() => {
            setIsRegister(!isRegister);
            setError(null);
          }}
          style={{
            border: "none",
            background: "none",
            color: "#0066cc",
            cursor: "pointer",
            textDecoration: "underline",
          }}
        >
          {isRegister ? "Sign In" : "Register"}
        </button>
      </p>
    </div>
  );
}
