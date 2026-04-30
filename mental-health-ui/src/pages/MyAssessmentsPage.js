import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/dashboard.css";
import UserHeader from "../components/UserHeader";
import { FiMaximize2, FiTrendingUp, FiTrendingDown } from "react-icons/fi";
import { FaRegCalendarAlt } from "react-icons/fa";
import { MdOutlineSpeed } from "react-icons/md";
import { BsGraphUp } from "react-icons/bs"; 
import { useNavigate } from "react-router-dom";

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
  const [dashboard, setDashboard] = useState(null);
  const [trendAnalysis, setTrendAnalysis] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const token = sessionStorage.getItem("token");
  const email = sessionStorage.getItem("email");
  const navigate = useNavigate();

  // =========================
  // FETCH DATA
  // =========================
  useEffect(() => {
    fetchDashboard();
    fetchTrendAnalysis();
  }, []);

  const fetchDashboard = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/api/v1/phq9/dashboard",
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setDashboard(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const fetchTrendAnalysis = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/api/v1/phq9/trend-analysis",
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTrendAnalysis(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================
  // LOADING STATE
  // =========================
  if (!dashboard) {
    return <p className="loading">Loading...</p>;
  }

  // =========================
  // 🚨 NEW USER (NO DATA)
  // =========================
  if (!dashboard.latest) {
    return (
      <div className="dashboard-container">
        <UserHeader />

        <div className="main-content">
          <div className="top-navbar">
            <h3 className="brand">Welcome</h3>
            <div className="user-email-box">{email}</div>
          </div>

          <div className="empty-state">
            <h2>No Assessments Yet</h2>
            <p>
              You haven’t taken any PHQ-9 assessment yet.
              Start your first assessment to see insights.
            </p>

            <button
              className="primary-btn"
              onClick={() => navigate("/assessment")}
            >
              Take Assessment
            </button>
          </div>
        </div>
      </div>
    );
  }

  // =========================
  // SAFE DATA
  // =========================
  const { latest, trend } = dashboard;

  const questionData = (latest.answers || []).map((val, i) => ({
    name: `Q${i + 1}`,
    value: val === 0 ? null : val
  }));

  // =========================
  // MAIN UI
  // =========================
  return (
    <div className="dashboard-container">
      <UserHeader />

      <div className="main-content">

        {/* TOP NAVBAR */}
        <div className="top-navbar">
        <h3 className="brand">Welcome</h3>

        <div className="nav-right">
          <button
            className="take-assessment-btn"
            onClick={() => navigate("/assessment")}
          >
            Take Assessment
          </button>

          <div className="user-email-box">
            {email}
          </div>
        </div>
      </div>

        {/* HEADER */}
        <div className="dashboard-header">
          <div>
            <h2 className="page-title">PHQ-9 Assessment</h2>
            <p className="subtitle">Summary of your submitted assessment</p>
          </div>

          <div className="assessment-date">
            <FaRegCalendarAlt />
            <div>
              <span>Assessment Date</span>
              <p>
                {trend?.history?.length > 0
                  ? trend.history[trend.history.length - 1].date
                  : "-"}
              </p>
            </div>
          </div>
        </div>

        {/* TOP CARDS */}
        <div className="top-cards">

          <div className="top-card">
            <div className="card-header">
              <p>Total PHQ-9 Score</p>
              <BsGraphUp className="icon purple" />
            </div>
            <h2>{latest.score}</h2>
            <span>out of 27</span>
          </div>

          <div className="top-card">
            <div className="card-header">
              <p>Severity</p>
              <MdOutlineSpeed className="icon orange" />
            </div>
            <h2 className="severity-text">{latest.severity}</h2>
          </div>

          <div className="top-card">
            <div className="card-header">
              <p>Previous</p>
              <FiTrendingDown className="icon blue" />
            </div>
            <h2>{trend?.previous_score ?? "-"}</h2>
          </div>

          <div className="top-card">
            <div className="card-header">
              <p>Change</p>
              <FiTrendingUp className="icon red" />
            </div>
            <h2 className="change-text">
              {trend?.previous_score !== null
                ? latest.score - trend.previous_score
                : "-"}
            </h2>
            <span>from previous</span>
          </div>

        </div>

        {/* CHARTS */}
        <div className="chart-section">

          <div className="chart-card">
            <h3>Question-wise Breakdown</h3>
            <ResponsiveContainer width="100%" height={170}>
              <BarChart data={questionData}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#7b6ef6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="chart-card">
            <h3>PHQ-9 Score Trend</h3>
            <ResponsiveContainer width="100%" height={170}>
              <LineChart data={trend?.history || []}>
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="score"
                  stroke="#7b6ef6"
                  strokeWidth={3}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

        </div>

        {/* BOTTOM */}
        <div className="bottom-section">

          <div className="box">
            <h3>Severity Scale</h3>
            <div className="scale">
              <span className="green">0–4 Minimal</span>
              <span className="blue">5–9 Mild</span>
              <span className="yellow">10–14 Moderate</span>
              <span className="red">15–27 Severe</span>
            </div>
            <p>
              Your score of <b>{latest.score}</b> falls in{" "}
              <b>{latest.severity}</b>
            </p>
          </div>

          <div className="box">
            <h3>Key Insights</h3>
            <p className="insight-text">{latest.insight}</p>
          </div>

          {/* DISORDER */}
          <div className="box disorder-box">
            <div className="disorder-header">
            <h3>Detected Disorder</h3>

            {trendAnalysis?.category && (
              <button
                className="expand-btn"
                onClick={() => setShowModal(true)}
              >
                <FiMaximize2 />
              </button>
            )}
          </div>

            {trendAnalysis?.category ? (
              <>
                <p><b>Category:</b> {trendAnalysis.category}</p>
                <p><b>Disorder:</b> {trendAnalysis.disorder}</p>
              </>
            ) : (
              <p>No disorder identified</p>
            )}
          </div>

        </div>

        {/* MODAL */}
        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>

              <button
                className="close-btn"
                onClick={() => setShowModal(false)}
              >
                ✕
              </button>

              <h2>Disorder Details</h2>

              <p><b>Category:</b> {trendAnalysis?.category}</p>
              <p><b>Disorder:</b> {trendAnalysis?.disorder}</p>

              <h3>AI Insight</h3>
              <p className="insight-text">
                {trendAnalysis?.insight || "No insight available"}
              </p>

              <h3>Recommendations</h3>

              {Array.isArray(trendAnalysis?.recommendation) ? (
                <ul className="recommendation-list">
                  {trendAnalysis.recommendation.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              ) : (
                <p>No recommendations available</p>
              )}

            </div>
          </div>
        )}

      </div>
    </div>
  );
}