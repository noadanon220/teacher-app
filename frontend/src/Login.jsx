import { useState } from "react";
import { request, setToken } from "./api";

export default function Login({ onLogin }) {
  const [name, setName] = useState("");
  const [idNumber, setIdNumber] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (!name.trim() || !/^\d{9}$/.test(idNumber)) {
      setError("Enter your name and a 9-digit ID number");
      return;
    }

    try {
      const data = await request("/login", {
        method: "POST",
        body: JSON.stringify({ name: name.trim(), id_number: idNumber }),
      });
      setToken(data.access_token);
      onLogin();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="login-page">
      <div className="brand">
        <svg width="34" height="34" viewBox="0 0 24 24" fill="none" aria-hidden="true">
          <path
            d="M12 2.5 20 7v10l-8 4.5L4 17V7l8-4.5Z M4 7l8 4.5L20 7 M12 11.5v10"
            stroke="#3b82f6"
            strokeWidth="2"
            strokeLinejoin="round"
          />
        </svg>
        <span>Student Management</span>
      </div>

      <form className="login-card" onSubmit={handleSubmit}>
        <p className="subtitle">Please enter your details</p>
        <h1 className="title">Welcome</h1>

        <input
          className="field"
          placeholder="Full name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          className="field"
          placeholder="ID number"
          value={idNumber}
          onChange={(e) => setIdNumber(e.target.value)}
          inputMode="numeric"
          maxLength={9}
        />

        {error && <p className="error">{error}</p>}

        <button className="btn-primary" type="submit">
          Log in
        </button>
      </form>
    </div>
  );
}
