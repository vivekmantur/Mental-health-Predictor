import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/doctor.css";
import ResultCard from "../components/ResultCard";

export default function DoctorDashboard() {
  const [patients, setPatients] = useState([]);
  const [assessments, setAssessments] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [selected, setSelected] = useState(null);

  const token = sessionStorage.getItem("token");

  // =========================
  // FETCH PATIENTS
  // =========================
  useEffect(() => {
    fetchPatients();
  }, []);

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
      console.error("Error fetching patients", err);
    }
  };

  // =========================
  // FETCH USER ASSESSMENTS
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
      console.error("Error fetching assessments", err);
    }
  };

  return (
    <div className="doctor-container">
      <h2 className="title">Patient Insights</h2>

      {/* =========================
          👇 PATIENT LIST VIEW
      ========================= */}
      {!selectedUser && (
        <div className="card-grid">
          {patients.map((user) => (
            <div
              key={user.user_id}
              className="card clickable"
              onClick={() => {
                setSelectedUser(user);
                fetchAssessments(user.user_id);
              }}
            >
              <h3>{user.email}</h3>
              <p><b>Latest Score:</b> {user.score}</p>
              <p><b>Severity:</b> {user.severity}</p>
              <p>
                <b>Last Updated:</b>{" "}
                {new Date(user.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* =========================
          👇 PATIENT ASSESSMENTS VIEW
      ========================= */}
      {selectedUser && (
        <>
          <button
            className="back-btn"
            onClick={() => {
              setSelectedUser(null);
              setAssessments([]);
            }}
          >
            ← Back to Patients
          </button>

          <h3 style={{ marginBottom: "15px" }}>
            {selectedUser.email}
          </h3>

          <div className="card-grid">
            {assessments.map((item) => (
              <div
                key={item.id}
                className="card clickable"
                onClick={() => setSelected(item)}
              >
                <p><b>Score:</b> {item.score}</p>
                <p><b>Severity:</b> {item.severity}</p>
                <p>
                  <b>Date:</b>{" "}
                  {new Date(item.created_at).toLocaleDateString()}
                </p>

                <div className={`status ${item.status}`}>
                  {item.status}
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* =========================
          👇 MODAL (UNCHANGED)
      ========================= */}
      {selected && (
        <div className="modal-overlay" onClick={() => setSelected(null)}>
          <div
            className="modal-content"
            onClick={(e) => e.stopPropagation()}
          >
            <button className="close-btn" onClick={() => setSelected(null)}>
              ✖
            </button>

            <ResultCard
              data={selected}
              status={selected.status}
            />
          </div>
        </div>
      )}
    </div>
  );
}