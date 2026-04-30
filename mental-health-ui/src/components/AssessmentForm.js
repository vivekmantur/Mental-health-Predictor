import React, { useState } from "react";
import axios from "axios";
import "../styles/assessmentform.css";
import { useNavigate } from "react-router-dom";

const questions = [
  "Little interest or pleasure in doing things",
  "Feeling down, depressed, or hopeless",
  "Trouble falling or staying asleep, or sleeping too much",
  "Feeling tired or having little energy",
  "Poor appetite or overeating",
  "Feeling bad about yourself — or that you are a failure",
  "Trouble concentrating on things",
  "Moving or speaking slowly or being restless",
  "Thoughts that you would be better off dead or hurting yourself"
];

const options = [
  { label: "Not at all", value: 0 },
  { label: "Several days", value: 1 },
  { label: "More than half the days", value: 2 },
  { label: "Nearly every day", value: 3 }
];

export default function AssessmentForm() {
  const [answers, setAnswers] = useState(Array(9).fill(null));
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (qIndex, value) => {
    const updated = [...answers];
    updated[qIndex] = value;
    setAnswers(updated);
  };

  const handleSubmit = async () => {
    if (answers.includes(null)) {
      alert("Please answer all questions");
      return;
    }

    setLoading(true);
    const token = sessionStorage.getItem("token");

    try {
      await axios.post(
        `http://localhost:8000/api/v1/phq9/submit`,
        { answers, notes },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json"
          }
        }
      );

      navigate("/my-assessments");
    } catch (error) {
      console.error(error);
      alert("Error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <h2 className="title">PHQ-9 Assessment</h2>

      {/* ✅ QUESTIONS */}
      <div className="questions-container">
        {questions.map((q, index) => (
          <div className="question-row" key={index}>

            {/* LEFT SIDE → QUESTION */}
            <div className="question-text">
              {index + 1}. {q}
            </div>

            {/* RIGHT SIDE → OPTIONS */}
            <div className="options-row">
              {options.map((opt) => (
                <label key={opt.value} className="radio-inline">
                  <input
                    type="radio"
                    name={`q${index}`}
                    checked={answers[index] === opt.value}
                    onChange={() => handleChange(index, opt.value)}
                  />
                  {opt.label}
                </label>
              ))}
            </div>

          </div>
        ))}
      </div>

      {/* ✅ NOTES */}
      <div className="notes-card">
        <div className="question-text">Additional Notes (Optional)</div>
        <textarea
          className="notes-box"
          placeholder="Enter any additional thoughts..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />
      </div>

      {/* ✅ SUBMIT */}
      <button className="submit-btn" onClick={handleSubmit}>
        {loading ? "Submitting..." : "Submit Assessment"}
      </button>
    </>
  );
}