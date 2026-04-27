import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AssessmentForm from "../components/AssessmentForm";
import bgImage from "../assets/mentalhealth.jpg";

export default function AssessmentPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    const user = JSON.parse(sessionStorage.getItem("user"));

    // ❌ Not logged in
    if (!token) {
      navigate("/login", { replace: true });
      return;
    }

    // ❌ Doctor trying to access patient page
    if (user?.usertype === "doctor") {
      navigate("/doctor", { replace: true });
      return;
    }

  }, [navigate]);

  return (
    <div
      className="assessment-hero"
      style={{
        backgroundImage: `url(${bgImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
      }}
    >
      <div className="overlay center-layout">
        <div className="form-glass-card">
          <AssessmentForm />
        </div>
      </div>
    </div>
  );
}