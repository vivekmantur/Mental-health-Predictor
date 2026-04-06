import React, { useState } from "react";
import "../styles/result.css";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar
} from "recharts";

export default function ResultCard({ result }) {

  const [expanded, setExpanded] = useState(false);

  if (!result) return null;

  const percentage = (result.score / 27) * 100;

  /* ✅ SINGLE SOURCE OF DATA */
  const chartData = [
    { subject: "Mood", value: result.ai_scores[1] || 0 },
    { subject: "Energy", value: result.ai_scores[3] || 0 },
    { subject: "Sleep", value: result.ai_scores[2] || 0 },
    { subject: "Focus", value: result.ai_scores[6] || 0 },
    { subject: "Self-worth", value: result.ai_scores[5] || 0 }
  ];

  /* 🔥 Convert text → points */
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

  /* 🎯 Severity color */
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "minimal": return "#22c55e";
      case "mild": return "#84cc16";
      case "moderate": return "#f59e0b";
      case "moderately severe": return "#f97316";
      case "severe": return "#ef4444";
      default: return "#6366f1";
    }
  };

  return (
    <div className="result-card">

      {/* ===== TITLE ===== */}
      <h3>Your Mental Health Report</h3>

      {/* ===== SCORE BAR ===== */}
      <div className="meter-bar">
        <div
          className="meter-fill"
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* ===== SCORE + SEVERITY ===== */}
      <div className="score-row">
        <span>{result.score}/27</span>

        <span
          className="severity-badge"
          style={{ background: getSeverityColor(result.severity) }}
        >
          {result.severity}
        </span>
      </div>

      {/* ===== CHART SECTION ===== */}
      <div className="result-section">

        <div className="chart-header">
          <h4>Mental Health Overview</h4>

          <button className="expand-btn" onClick={() => setExpanded(true)}>
            ⤢
          </button>
        </div>

        <div className="chart-row">

          {/* 🔵 RADAR CHART */}
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={260}>
              <RadarChart data={chartData}>
                <PolarGrid stroke="#aaa" />
                <PolarAngleAxis
                  dataKey="subject"
                  tick={{ fill: "#fff", fontSize: 12 }}
                />
                <PolarRadiusAxis
                  domain={[0, 3]}
                  tick={{ fill: "#ccc" }}
                />
                <Radar
                  dataKey="value"
                  stroke="#06b6d4"
                  fill="#06b6d4"
                  fillOpacity={0.5}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          {/* 🟣 BAR CHART */}
          <div className="chart-box">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart
                data={chartData}
                margin={{ top: 10, right: 20, left: 0, bottom: 40 }}
              >
                <XAxis
                  dataKey="subject"
                  interval={0}   // ✅ SHOW ALL LABELS
                  stroke="#fff"
                  tick={{ fill: "#fff", fontSize: 12 }}
                />
                <YAxis
                  domain={[0, 3]}
                  stroke="#fff"
                  tick={{ fill: "#fff" }}
                />
                <Tooltip />
                <Bar
                  dataKey="value"
                  fill="#4f46e5"
                  radius={[6, 6, 0, 0]}
                />
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
            <div key={i} className="insight-card">
              {item}
            </div>
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

      {/* ===== FULL SCREEN MODAL ===== */}
      {expanded && (
        <div className="modal-overlay">

          <div className="modal-content">

            <button
              className="close-btn"
              onClick={() => setExpanded(false)}
            >
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
                <BarChart
                  data={chartData}
                  margin={{ top: 10, right: 20, left: 0, bottom: 40 }}
                >
                  <XAxis
                    dataKey="subject"
                    interval={0}
                    stroke="#fff"
                    tick={{ fill: "#fff", fontSize: 12 }}
                  />
                  <YAxis stroke="#fff" tick={{ fill: "#fff" }} />
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