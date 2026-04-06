import React, { useState } from "react";
import AssessmentForm from "../components/AssessmentForm";
import ResultCard from "../components/ResultCard";
import bgImage from "../assets/mentalhealth.jpg";

export default function AssessmentPage() {
  const [result, setResult] = useState(null);

  return (
    <div
      className="assessment-hero"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className={`overlay ${result ? "split-layout" : "center-layout"}`}>

        {/* LEFT FORM */}
        <div className="left-panel">
          <div className="form-glass-card">
            <AssessmentForm onResult={setResult} />
          </div>
        </div>

        {/* RIGHT RESULT */}
        {result && (
          <div className="right-panel">
            <div className="result-wrapper">
              <ResultCard result={result} />
            </div>
          </div>
        )}

      </div>
    </div>
  );
}