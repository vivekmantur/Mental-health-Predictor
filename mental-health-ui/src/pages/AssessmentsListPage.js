import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/assessment.css";
import UserHeader from "../components/UserHeader";

export default function AssessmentListPage() {
  const [assessments, setAssessments] = useState([]);
  const [selected, setSelected] = useState(null);

  const token = sessionStorage.getItem("token");

  // ✅ Get user email safely
  const user = JSON.parse(sessionStorage.getItem("user"));

  useEffect(() => {
    fetchAssessments();
  }, []);

  const fetchAssessments = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/api/v1/phq9/my-assessments",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setAssessments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="dashboard-container assessments-page">

      {/* ✅ SIDEBAR */}
      <UserHeader />

      {/* ✅ MAIN CONTENT */}
      <div className="main-content">

        {/* 🔥 TOP NAVBAR */}
        <div className="top-navbar">
          <div className="top-left">
            <h3 className="brand">Welcome</h3>
          </div>

          <div className="top-right">
            <div className="user-email-box">
              {user?.email || "user@email.com"}
            </div>
          </div>
        </div>

        {/* PAGE TITLE */}
        <h2 className="page-title">My Assessments</h2>

        {/* TABLE */}
        <div className="table-container">

          <table>
            <thead>
              <tr>
                <th>Submitted Date</th>
                <th>Score</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>

            <tbody>
              {assessments.length === 0 ? (
                <tr>
                  <td colSpan="5">No assessments found</td>
                </tr>
              ) : (
                assessments.map((item) => (
                  <tr key={item.id}>

                    {/* DATE */}
                    <td>
                      {new Date(item.created_at).toLocaleDateString()}
                    </td>

                    <td>{item.score}</td>
                    <td>{item.severity}</td>

                    {/* STATUS */}
                    <td>
                      <span className={`status-badge ${item.status}`}>
                        {item.status}
                      </span>
                    </td>

                    {/* ACTION */}
                    <td>
                      {item.status === "success" && item.approved_at ? (
                        <>
                          <button
                            className="view-btn"
                            onClick={() => setSelected(item)}
                          >
                            View
                          </button>

                          <div className="approved-date">
                            Approved on:{" "}
                            {new Date(item.approved_at).toLocaleDateString()}
                          </div>
                        </>
                      ) : (
                        <span className="pending-text">
                          Waiting for doctor approval
                        </span>
                      )}
                    </td>

                  </tr>
                ))
              )}
            </tbody>
          </table>

        </div>

        {/* 🔥 MODAL */}
        {selected && (
          <div className="modal-overlay" onClick={() => setSelected(null)}>

            <div className="modal" onClick={(e) => e.stopPropagation()}>

              {/* CLOSE */}
              <button
                className="modal-close"
                onClick={() => setSelected(null)}
              >
                ✕
              </button>

              <h3>Assessment Details</h3>

              <p><strong>Score:</strong> {selected.score}</p>
              <p><strong>Severity:</strong> {selected.severity}</p>

              {/* INSIGHT */}
              <div>
                <strong>Insight:</strong>
                <p>{selected.insight}</p>
              </div>

              {/* RECOMMENDATION */}
              <div>
                <strong>Recommendation:</strong>

                <div className="recommendation-box">
                  <ul>
                    {selected.recommendation
                      ?.split("\n")
                      .filter(line => line.trim() !== "")
                      .map((line, index) => (
                        <li key={index}>
                          {line.replace(/^[-•*\d.\s]+/, "").replace(/\*\*/g, "")}
                        </li>
                      ))}
                  </ul>
                </div>

              </div>
              {/* ✅ DOCTOR NOTES (ONLY IF SUCCESS) */}
                {selected.status === "success" && selected.doctor_notes && (
                <div>
                    <strong>Doctor Notes:</strong>

                    <div className="recommendation-box">
                    <p style={{ margin: 0 }}>
                        {selected.doctor_notes}
                    </p>
                    </div>
                </div>
                )}

            </div>
          </div>
        )}

      </div>
    </div>
  );
}