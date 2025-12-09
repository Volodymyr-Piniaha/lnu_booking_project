import { useState } from "react";
import "./Signup.css";

export default function Signup() {
  const [form, setForm] = useState({ name: "", email: "", password: "" });

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    fetch("http://<IP_BACKEND>:8000/api/signup/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        FullName: form.name,
        Email: form.email,
        Password: form.password
      })
    })
      .then(res => res.json())
      .then(data => {
        if (data.success) alert("Signup successful!");
        else alert("Error: " + data.message);
      })
      .catch(err => console.error(err));
  };

  return (
    <div className="page">
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input name="name" placeholder="Full Name" onChange={handleChange} />
        <input name="email" type="email" placeholder="Email" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />
        <button type="submit">Create Account</button>
      </form>
    </div>
  );
}
