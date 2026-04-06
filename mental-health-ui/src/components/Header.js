import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/header.css";
import logo from "../assets/cognine.png";

export default function Header() {
  const navigate = useNavigate();

  return (
    <div className="header-glass">
      <div className="header-container">

        {/* 🔥 LOGO */}
        <div className="logo-box" onClick={() => navigate("/")}>
          <img src={logo} alt="cognine" />
        </div>

      </div>
    </div>
  );
}