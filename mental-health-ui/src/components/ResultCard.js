import React, { useState, useEffect } from "react";
import axios from "axios";

export default function ResultCard({ data, status }) {
  const [editableData, setEditableData] = useState(null);

  const isEditable = status === "pending";

  useEffect(() => {
    setEditableData(data);

    // Auto resize textarea after render
    setTimeout(() => {
      const textareas = document.querySelectorAll(".textarea");
      textareas.forEach((ta) => {
        ta.style.height = "auto";
        ta.style.height = ta.scrollHeight + "px";
      });
    }, 0);
  }, [data]);

  if (!editableData) {
    return <div>Loading...</div>;
  }

  // ✅ Auto resize while typing
  const autoResize = (e) => {
    e.target.style.height = "auto";
    e.target.style.height = e.target.scrollHeight + "px";
  };

  // ✅ Handle input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setEditableData({
      ...editableData,
      [name]: value,
    });
  };

  // ✅ SAVE
  const handleSave = async () => {
    try {
      await axios.put(
        `http://localhost:8000/api/v1/doctor/assessments/${data.id}`,
        {
          score: editableData.score,
          severity: editableData.severity,
          insight: editableData.insight,
          recommendation: editableData.recommendation,
        },
        {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("token")}`,
          },
        }
      );

      alert("Saved successfully");
    } catch (err) {
      console.error(err);
      alert("Save failed");
    }
  };

  // ✅ CONFIRM
  const handleConfirm = async () => {
    try {
      // Step 1: Save content
      await axios.put(
        `http://localhost:8000/api/v1/doctor/assessments/${data.id}`,
        {
          score: editableData.score,
          severity: editableData.severity,
          insight: editableData.insight,
          recommendation: editableData.recommendation,
        },
        {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("token")}`,
          },
        }
      );

      // Step 2: Update status
      await axios.put(
        `http://localhost:8000/api/v1/doctor/assessments/${data.id}/status`,
        {
          status: "success",
        },
        {
          headers: {
            Authorization: `Bearer ${sessionStorage.getItem("token")}`,
          },
        }
      );

      alert("Confirmed successfully");

      // 🔥 Refresh UI
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Confirm failed");
    }
  };

  // ✅ Format bullets
  const formatText = (text) => {
    if (!text) return "";
    return text.replace(/\*\*(.*?)\*\*/g, "\n🔹 $1\n");
  };

  return (
    <div className="result-card">
      <h2 className="email">{editableData.email}</h2>

      <div className="row">
        <div className="field">
          <label>Score</label>
          <input
            type="number"
            name="score"
            value={editableData.score || ""}
            onChange={handleChange}
            disabled={!isEditable}
          />
        </div>

        <div className="field">
          <label>Severity</label>
          <input
            type="text"
            name="severity"
            value={editableData.severity || ""}
            onChange={handleChange}
            disabled={!isEditable}
          />
        </div>
      </div>

      {/* Insight */}
      <div className="field">
        <label>Insight</label>

        {isEditable ? (
          <textarea
            name="insight"
            value={editableData.insight || ""}
            onChange={(e) => {
              handleChange(e);
              autoResize(e);
            }}
            className="textarea"
          />
        ) : (
          <div className="text-display">
            {editableData.insight}
          </div>
        )}
      </div>

      {/* Recommendation */}
      <div className="field">
        <label>Recommendation</label>

        {isEditable ? (
          <textarea
            name="recommendation"
            value={editableData.recommendation || ""}
            onChange={(e) => {
              handleChange(e);
              autoResize(e);
            }}
            className="textarea"
          />
        ) : (
          <div className="text-display">
            {formatText(editableData.recommendation)}
          </div>
        )}
      </div>

      {isEditable && (
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
  );
}