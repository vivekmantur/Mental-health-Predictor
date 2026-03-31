import React, { useState } from "react";
import AssessmentForm from "./components/AssessmentForm";
import ResultCard from "./components/ResultCard";
import "./styles/layout.css";

function App() {
  const [result, setResult] = useState(null);

  return (
    <div className="app-bg">

      {/* ✅ FIXED HEADER */}
      <div className="header">
        <div className="header-inner">
          <h1>Mental Health Assessment</h1>
          <p>Understand your mental well-being using AI insights</p>
        </div>
      </div>

      {/* MAIN */}
      <div className={`main-container ${result ? "split" : "center"}`}>

        <div className="form-card">
          <AssessmentForm onResult={setResult} />
        </div>

        {result && (
          <div className="result-card-container">
            <ResultCard result={result} />
          </div>
        )}

      </div>

      {/* ✅ FIXED FOOTER */}
      <div className="footer">
        <div className="footer-inner">
          © 2026 Mental Health AI Platform
        </div>
      </div>

    </div>
  );
}

export default App;