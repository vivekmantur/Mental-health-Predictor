import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";
import { FiMaximize2, FiMinimize2 } from "react-icons/fi";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from "recharts";

export default function MyAssessmentsPage() {
  const [data, setData] = useState([]);
  const [selected, setSelected] = useState(null);
  const [trendData, setTrendData] = useState(null);
  const [expanded, setExpanded] = useState(false);

  const navigate = useNavigate();
  const token = sessionStorage.getItem("token");

  const latestSuccess = data
    .filter((item) => item.status === "success")
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))[0];

  useEffect(() => {
    fetchData();
    fetchTrend();
  }, []);

  const fetchData = async () => {
    try {
      const res = await axios.get(
        `http://localhost:8000/api/v1/phq9/my-assessments`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setData(res.data || []);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTrend = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/api/v1/phq9/trend-analysis",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setTrendData(res.data || null);
    } catch (err) {
      console.error(err);
    }
  };

  const successAssessments = data
    .filter((item) => item.status === "success")
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at));

  const chartData = successAssessments.map((item) => ({
    date: new Date(item.created_at).toLocaleDateString(),
    score: item.score,
  }));

  const severityCount = {};
  data.forEach((item) => {
    if (item.status === "success") {
      severityCount[item.severity] =
        (severityCount[item.severity] || 0) + 1;
    }
  });

  const severityData = Object.keys(severityCount).map((key) => ({
    severity: key,
    count: severityCount[key],
  }));

  const getSeverityRange = (score) => {
    if (!score && score !== 0) return "Unknown";
    if (score <= 4) return "Minimal";
    if (score <= 9) return "Mild";
    if (score <= 14) return "Moderate";
    return "Severe";
  };

  // ✅ UNIVERSAL SAFE RENDER
  const renderRecommendation = (rec) => {
    if (!rec) return <p>No recommendation available</p>;

    if (typeof rec === "string") {
      return <p>{rec}</p>;
    }

    if (Array.isArray(rec)) {
      return (
        <ul>
          {rec.map((item, i) => (
            <li key={i}>{String(item)}</li>
          ))}
        </ul>
      );
    }

    if (typeof rec === "object") {
      return (
        <div>
          {Object.entries(rec).map(([key, value]) => (
            <div key={key} style={{ marginBottom: "10px" }}>
              <b>{key}</b>
              <p>{String(value)}</p>
            </div>
          ))}
        </div>
      );
    }

    return <p>{String(rec)}</p>;
  };

  return (
    <div className="dashboard-container">

      {/* HEADER */}
      <div className="dashboard-header">
        <h2>My Assessments</h2>

        <button
          className="new-assessment-btn"
          onClick={() => navigate("/assessment")}
        >
          + Check your mental health now
        </button>
      </div>

      <div className="dashboard-wrapper">

        {/* LEFT */}
        <div className="dashboard-left">
          <div className="card-grid">
            {data.map((item) => (
              <div key={item.id} className="card">
                <h3>{item.severity}</h3>
                <p><b>Score:</b> {item.score}</p>

                <p>
                  <b>Status:</b>{" "}
                  <span
                    style={{
                      color: item.status === "success" ? "green" : "orange",
                      fontWeight: "600",
                    }}
                  >
                    {item.status}
                  </span>
                </p>

                {item.status === "success" && (
                  <button
                    className="view-btn"
                    onClick={() => setSelected(item)}
                  >
                    View Result
                  </button>
                )}

                {item.status === "pending" && (
                  <p className="pending-text">
                    Waiting for doctor approval...
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT */}
        <div className="dashboard-right">
          {expanded && (
            <div
              className="modal-backdrop-custom"
              onClick={() => setExpanded(false)}
            />
          )}

          <div className={`trend-card ${expanded ? "expanded" : ""}`}>

            <div className="trend-header">
              <h3>Your Mental Health Insight</h3>

              <button
                className="expand-btn"
                onClick={() => setExpanded(!expanded)}
              >
                {expanded ? <FiMinimize2 /> : <FiMaximize2 />}
              </button>
            </div>

            {!trendData?.insight ? (
              <p>Not enough data yet</p>
            ) : (
              <>
                <div className="summary">
                  <p><b>Latest:</b> {trendData?.latest_score}</p>
                  <p><b>Previous:</b> {trendData?.previous_score}</p>
                </div>

                {latestSuccess?.disorder && (
                  <p>
                    <b>Detected Condition:</b>{" "}
                    <span style={{ color: "#2c7be5", fontWeight: "600" }}>
                      {latestSuccess.disorder}
                    </span>
                  </p>
                )}

                <p>
                  <b>Current Status:</b>{" "}
                  {getSeverityRange(trendData?.latest_score)}
                </p>

                <div className="trend-indicator">
                  {trendData?.previous_score > trendData?.latest_score ? (
                    <p className="improved">⬇ Improving</p>
                  ) : (
                    <p className="worsened">⬆ Needs Attention</p>
                  )}
                </div>

                <div className="result-box">
                  <h4>Insight</h4>
                  <p>{trendData?.insight}</p>
                </div>

                <div className="result-box">
                  <h4>Recommendation</h4>
                  {renderRecommendation(trendData?.recommendation)}
                </div>
              </>
            )}

            {/* Charts */}
            <h4 style={{ marginTop: "20px" }}>Mood Trend</h4>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={chartData}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="score" strokeWidth={3} />
              </LineChart>
            </ResponsiveContainer>

            <h4 style={{ marginTop: "20px" }}>Severity Distribution</h4>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={severityData}>
                <XAxis dataKey="severity" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" />
              </BarChart>
            </ResponsiveContainer>

          </div>
        </div>
      </div>

      {/* MODAL */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>

            <button className="close-btn" onClick={() => setSelected(null)}>
              ✖
            </button>

            <h2>Assessment Result</h2>

            <p><b>Score:</b> {selected?.score}</p>
            <p><b>Severity:</b> {selected?.severity}</p>

            <hr />

            <div className="result-box">
              <h4>Insight</h4>
              <p>{selected?.insight}</p>
            </div>

            <div className="result-box">
              <h4>Recommendation</h4>
              {renderRecommendation(selected?.recommendation)}
            </div>

          </div>
        </div>
      )}
    </div>
  );
}