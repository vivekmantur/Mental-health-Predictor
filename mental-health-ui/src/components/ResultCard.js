import React, { useState } from "react";
import "../styles/result.css";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from "recharts";

export default function ResultCard({ result }) {

  const [expanded, setExpanded] = useState(false);
  const percentage = (result.score / 27) * 100;

  const toPoints = (text) => {
    if (!text) return [];
    return text
      .replace(/\*\*/g, "")
      .split(/\d+\.\s|\.\s/)
      .map(t => t.trim())
      .filter(t => t.length > 25);
  };

  const insights = toPoints(result.insight).slice(0, 4);
  const actions = toPoints(result.recommendation).slice(0, 5);

  const chartData = [
    { subject: "Mood", value: result.ai_scores[1] },
    { subject: "Energy", value: result.ai_scores[3] },
    { subject: "Sleep", value: result.ai_scores[2] },
    { subject: "Focus", value: result.ai_scores[6] },
    { subject: "Self-worth", value: result.ai_scores[5] }
  ];

  return (
    <div className="result-card">

      <h3>Your Mental Health Report</h3>

      {/* SCORE */}
      <div className="meter-bar">
        <div className="meter-fill" style={{ width: `${percentage}%` }} />
      </div>

      <div className="score-row">
        <span>{result.score}/27</span>
        <span className={`severity ${result.severity.toLowerCase()}`}>
          {result.severity}
        </span>
      </div>

      {/* ===== CHARTS ===== */}
      <div className="result-section">

        <div className="chart-header">
          <h4>Mental Health Overview</h4>

          <button className="expand-btn" onClick={() => setExpanded(true)}>
            ⤢
          </button>
        </div>

        <div className="chart-row">

          {/* RADAR */}
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={230}>
              <RadarChart data={chartData} margin={{ top: 10 }}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" tick={{ fontSize: 12 }} />
                <PolarRadiusAxis domain={[0, 3]} />
                <Radar
                  dataKey="value"
                  stroke="#6366f1"
                  fill="#6366f1"
                  fillOpacity={0.5}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* BAR */}
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={230}>
              <BarChart data={chartData}>
                <XAxis dataKey="subject" interval={0} />
                <YAxis domain={[0, 3]} />
                <Tooltip />
                <Bar dataKey="value" fill="#4f46e5" radius={[6,6,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>

        <p className="chart-hint">
          Radar shows balance • Bars show intensity
        </p>
      </div>

      {/* ===== INSIGHTS ===== */}
      <div className="result-section">
        <h4>Insights</h4>
        <div className="insight-grid">
          {insights.map((item, i) => (
            <div key={i} className="insight-card">{item}</div>
          ))}
        </div>
      </div>

      {/* ===== ACTION PLAN ===== */}
      <div className="result-section">
        <h4>What You Can Do</h4>
        <ul className="action-list">
          {actions.map((item, i) => (
            <li key={i}>{item}</li>
          ))}
        </ul>
      </div>

      {/* ===== MODAL ===== */}
      {expanded && (
        <div className="modal-overlay">

          <div className="modal-content">

            <button className="close-btn" onClick={() => setExpanded(false)}>
              ✕
            </button>

            <h3>Detailed Mental Health Analysis</h3>

            <div className="modal-charts">

              {/* RADAR */}
              <ResponsiveContainer width="50%" height={400}>
                <RadarChart data={chartData}>
                  <PolarGrid stroke="#ccc" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: "#fff" }} />
                  <PolarRadiusAxis domain={[0, 3]} tick={{ fill: "#fff" }} />
                  <Radar
                    dataKey="value"
                    stroke="#60a5fa"
                    fill="#60a5fa"
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>

              {/* BAR */}
              <ResponsiveContainer width="50%" height={400}>
                <BarChart data={chartData}>
                  <XAxis dataKey="subject" stroke="#fff" />
                  <YAxis stroke="#fff" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#60a5fa" />
                </BarChart>
              </ResponsiveContainer>

            </div>

          </div>
        </div>
      )}

    </div>
  );
}