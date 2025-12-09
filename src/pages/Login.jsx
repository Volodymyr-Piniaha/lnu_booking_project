import { useState } from "react";
import "./Login.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://<IP_BACKEND>:8000/api/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) alert("Login successful!");
        else alert("Invalid credentials");
      })
      .catch(err => console.error(err));
  };

  return (
    <div className="page">
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
        <button type="submit">Log In</button>
      </form>
    </div>
  );
}
