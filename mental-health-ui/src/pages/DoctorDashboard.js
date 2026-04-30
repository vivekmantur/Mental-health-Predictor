import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/doctor.css";
import "../styles/assessment.css";
import UserHeader from "../components/UserHeader";

export default function DoctorDashboard() {
  const [patients, setPatients] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [selected, setSelected] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({});

  const token = sessionStorage.getItem("token");
  const user = JSON.parse(sessionStorage.getItem("user"));

  // =========================
  // FETCH PATIENTS
  // =========================
  const fetchPatients = async () => {
    try {
      const res = await axios.get(
        "http://localhost:8000/api/v1/doctor/patients-list",
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setPatients(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // =========================
  // FETCH ASSESSMENTS
  // =========================
  const fetchAssessments = async (userId) => {
    try {
      const res = await axios.get(
        `http://localhost:8000/api/v1/doctor/patient-assessments/${userId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setAssessments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  // RESET EVENT
  useEffect(() => {
    const handleReset = () => {
      setSelectedUser(null);
      setAssessments([]);
      setSelected(null);
    };

    window.addEventListener("resetDoctor", handleReset);
    return () => window.removeEventListener("resetDoctor", handleReset);
  }, []);

  // MODAL OPEN
  const openModal = (item) => {
    setSelected(item);
    setFormData({ ...item });
    setEditMode(item.status === "pending");
  };

  // SAVE
  const handleSave = async () => {
    try {
      await axios.put(
        `http://localhost:8000/api/v1/doctor/assessments/${formData.id}`,
        {
          score: formData.score,
          severity: formData.severity,
          insight: formData.insight,
          recommendation: formData.recommendation,
          doctor_notes: formData.doctor_notes,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      alert("Saved successfully");
    } catch (err) {
      console.error(err);
      alert("Error saving");
    }
  };

  // CONFIRM
  const handleConfirm = async () => {
    try {
      await axios.put(
        `http://localhost:8000/api/v1/doctor/assessments/${formData.id}/status`,
        { status: "success" },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      alert("Approved successfully");
      setSelected(null);
      fetchAssessments(selectedUser.user_id);
    } catch (err) {
      console.error(err);
      alert("Error approving");
    }
  };

  return (
    <div className="dashboard-container">
      {/* SIDEBAR */}
      <UserHeader />

      <div className="main-content">
        {/* TOP NAVBAR */}
        <div className="top-navbar">
          <h3 className="brand">Welcome</h3>
          <div className="user-email-box">
            {user?.email || "doctor@cognine.com"}
          </div>
        </div>

        {/* =========================
            PATIENT LIST
        ========================= */}
        {!selectedUser && (
          <div className="doctor-grid">
            {patients.map((u) => (
              <div
                key={u.user_id}
                className="doctor-card clickable"
                onClick={() => {
                  setSelectedUser(u);
                  fetchAssessments(u.user_id);
                }}
              >
                <h3 className="email">{u.email}</h3>

                <div className="card-row">
                  <span>Score</span>
                  <b>{u.score}</b>
                </div>

                <div className="card-row">
                  <span>Severity</span>
                  <b>{u.severity}</b>
                </div>

                <div className="card-row">
                  <span>Last Updated</span>
                  <b>{new Date(u.created_at).toLocaleDateString()}</b>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* =========================
            PATIENT ASSESSMENTS TABLE
        ========================= */}
        {selectedUser && (
          <div className="assessments-page">

            {/* BACK BUTTON */}
            <button
              className="view-btn"
              style={{ marginBottom: "10px" }}
              onClick={() => {
                setSelectedUser(null);
                setAssessments([]);
              }}
            >
              ← Back to Users
            </button>

            <h3 style={{ marginBottom: "12px" }}>
              {selectedUser.email}
            </h3>

            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Score</th>
                    <th>Severity</th>
                    <th>Status</th>
                    <th>Approved Date</th>
                    <th>Action</th>
                  </tr>
                </thead>

                <tbody>
                  {assessments.length === 0 ? (
                    <tr>
                      <td colSpan="6">No assessments found</td>
                    </tr>
                  ) : (
                    assessments.map((item) => (
                      <tr key={item.id}>

                        <td>
                          {new Date(item.created_at).toLocaleDateString()}
                        </td>

                        <td>{item.score}</td>

                        <td>{item.severity}</td>

                        <td>
                          <span className={`status-badge ${item.status}`}>
                            {item.status}
                          </span>
                        </td>

                        <td>
                          {item.status === "success" && item.approved_at
                            ? new Date(item.approved_at).toLocaleDateString()
                            : "-"}
                        </td>

                        <td>
                          <button
                            className="view-btn"
                            onClick={() => openModal(item)}
                          >
                            View
                          </button>
                        </td>

                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* =========================
            MODAL
        ========================= */}
        {selected && (
          <div
            className="modal-overlay"
            onClick={() => setSelected(null)}
          >
            <div
              className="modal doctor-modal"
              onClick={(e) => e.stopPropagation()}
            >
              <button
                className="modal-close"
                onClick={() => setSelected(null)}
              >
                ✕
              </button>

              <h3 className="modal-title">Assessment Details</h3>

              <div className="modal-row">
                <div className="field">
                  <label>Score</label>
                  <input
                    type="number"
                    value={formData.score || ""}
                    disabled={!editMode}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        score: e.target.value,
                      })
                    }
                  />
                </div>

                <div className="field">
                  <label>Severity</label>
                  <input
                    value={formData.severity || ""}
                    disabled={!editMode}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        severity: e.target.value,
                      })
                    }
                  />
                </div>
              </div>

              <div className="field">
                <label>Insight</label>
                {editMode ? (
                  <textarea
                    value={formData.insight || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        insight: e.target.value,
                      })
                    }
                  />
                ) : (
                  <div className="text-display">
                    {formData.insight}
                  </div>
                )}
              </div>

              <div className="field">
                <label>Recommendation</label>
                {editMode ? (
                  <textarea
                    value={formData.recommendation || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        recommendation: e.target.value,
                      })
                    }
                  />
                ) : (
                  <ul className="recommendation-list">
                    {formData.recommendation
                      ?.split("\n")
                      .filter((l) => l.trim())
                      .map((l, i) => (
                        <li key={i}>
                          {l.replace(/^[-•*\d.\s]+/, "")}
                        </li>
                      ))}
                  </ul>
                )}
              </div>

              <div className="field">
                <label>Doctor Notes</label>
                {editMode ? (
                  <textarea
                    value={formData.doctor_notes || ""}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        doctor_notes: e.target.value,
                      })
                    }
                  />
                ) : (
                  <div className="text-display">
                    {formData.doctor_notes || "No notes"}
                  </div>
                )}
              </div>

              {editMode && (
                <div className="btn-group">
                  <button className="save-btn" onClick={handleSave}>
                    Save
                  </button>

                  <button className="confirm-btn" onClick={handleConfirm}>
                    Confirm
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}