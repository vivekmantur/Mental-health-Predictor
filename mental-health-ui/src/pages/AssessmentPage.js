import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AssessmentForm from "../components/AssessmentForm";
import UserHeader from "../components/UserHeader";
import "../styles/assessmentform.css";   // form styles
import "../styles/assessment.css";       // top navbar styles

export default function AssessmentPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    const user = JSON.parse(sessionStorage.getItem("user"));

    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    if (user?.usertype === "doctor") {
      navigate("/doctor", { replace: true });
      return;
    }
  }, [navigate]);

  const user = JSON.parse(sessionStorage.getItem("user"));

  return (
    <div className="dashboard-container">

      {/* ✅ SIDEBAR */}
      <UserHeader />

      {/* ✅ MAIN CONTENT */}
      <div className="main-content">

        {/* ✅ TOP NAVBAR */}
        <div className="top-navbar">
          <h3 className="brand">Assessment</h3>
          <div className="user-email-box">
            {user?.email}
          </div>
        </div>

        {/* ✅ FORM */}
        <div style={{ padding: "20px" }}>
          <div className="form-glass-card">
            <AssessmentForm />
          </div>
        </div>

      </div>
    </div>
  );
}