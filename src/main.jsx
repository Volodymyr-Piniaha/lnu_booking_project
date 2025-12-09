import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Halls from "./pages/Halls";
import HallSchedule from "./pages/HallSchedule";
import MyBookings from "./pages/MyBookings";
import Navbar from "./components/Navbar";

import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Navbar /> {/* Navbar завжди зверху */}
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/halls" element={<Halls />} />
      <Route path="/schedule/:hallId" element={<HallSchedule />} />
      <Route path="/bookings" element={<MyBookings />} />
    </Routes>
  </BrowserRouter>
);
