import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";
import bgImage from "../assets/mentalhealth.jpg"; // ✅ IMPORTANT

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <div
      className="dashboard-hero"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="overlay">
        <div className="hero-content">
          <h1>Take Control of Your Mental Health</h1>

          <p>
            Take the PHQ-9 assessment and understand your emotional well-being
          </p>

          <button
            className="hero-btn"
            onClick={() => navigate("/assessment")}
          >
            Check Now →
          </button>
        </div>
      </div>
    </div>
  );
}