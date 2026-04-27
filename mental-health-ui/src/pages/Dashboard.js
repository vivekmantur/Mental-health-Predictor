import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/landing.css";
import bgImage from "../assets/mentalhealth.jpg";

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
      <div className="dashboard-overlay">
        <div className="hero-orb hero-orb-one" />
        <div className="hero-orb hero-orb-two" />

        <div className="hero-shell">
          <div className="dashboard-panel">
            <span className="hero-eyebrow">Talk to yourself like you would to someone you love.</span>

          <h1>Take Control of Your Mental Health</h1>

          <p>
            Complete the PHQ-9 assessment and turn feelings into a clearer,
            calmer starting point for action.
          </p>

            <div className="hero-actions">
              <button
                className="hero-btn"
                onClick={() => navigate("/assessment")}
              >
                Start PHQ-9
              </button>

              
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}