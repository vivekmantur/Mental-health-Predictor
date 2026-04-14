import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/header.css";
import logo from "../assets/cognine-transparent.png";

export default function Header() {
  const navigate = useNavigate();

  return (
    <header className="header-glass">
      <div className="header-container">
        <button
          type="button"
          className="brand-lockup"
          onClick={() => navigate("/")}
          aria-label="Go to dashboard"
        >
          <span className="logo-stage">
            <img src={logo} alt="Cognine" />
          </span>
        </button>
      </div>
    </header>
  );
}