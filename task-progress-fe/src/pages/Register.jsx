import React, { useState } from "react";
import { AuthAPI } from "../api/auth.api";
import { useNavigate } from "react-router-dom";
import "../Auth.css";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", email: "", password: "", password2: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setLoading(true);
    try {
      await AuthAPI.register(form.username, form.email, form.password, form.password2);
      // Auto-login after registration
      const res = await AuthAPI.login(form.username, form.password);
      localStorage.setItem("access_token", res.data.access);
      localStorage.setItem("refresh_token", res.data.refresh);
      navigate("/"); // redirect to home
    } catch (err) {
      setError(JSON.stringify(err.response?.data) || "Registration failed");
    } finally { setLoading(false); }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Sign Up</h2>
        {error && <div className="error">{error}</div>}
        <form onSubmit={handleSubmit}>
          <input type="text" name="username" placeholder="Username" value={form.username} onChange={handleChange} required />
          <input type="email" name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
          <input type="password" name="password" placeholder="Password" value={form.password} onChange={handleChange} required />
          <input type="password" name="password2" placeholder="Confirm Password" value={form.password2} onChange={handleChange} required />
          <button type="submit" disabled={loading}>{loading ? "Creating Account..." : "Register"}</button>
        </form>
        <p className="switch-text">
          Already have an account? <span onClick={() => navigate("/login")}>Login</span>
        </p>
      </div>
    </div>
  );
}