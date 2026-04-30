import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "../styles/userheader.css";
import logo from "../assets/cognine.png";

export default function UserHeader() {
  const navigate = useNavigate();
  const location = useLocation();

  const user = JSON.parse(sessionStorage.getItem("user"));
  const isDoctor = user?.usertype === "doctor";

  const logout = () => {
    sessionStorage.clear();
    navigate("/");
  };

  return (
    <div className="sidebar">

      {/* ✅ LOGO */}
      <div className="logo-container">
        <img src={logo} alt="cognine" className="logo-img" />
      </div>

      {/* ✅ MENU */}
      <div className="menu">

        {/* 👨‍⚕️ DOCTOR MENU */}
        {isDoctor ? (
          <>
            <button
              className={location.pathname === "/doctor" ? "active" : ""}
              onClick={() => {
                if (location.pathname === "/doctor") {
                    window.dispatchEvent(new Event("resetDoctor"));
                } else {
                    navigate("/doctor");
                }
                }}
            >
              Users
            </button>
          </>
        ) : (
          <>
            {/* 👤 PATIENT MENU */}
            <button
              className={location.pathname === "/my-assessments" ? "active" : ""}
              onClick={() => navigate("/my-assessments")}
            >
              Dashboard
            </button>

            <button
              className={location.pathname === "/assessments" ? "active" : ""}
              onClick={() => navigate("/assessments")}
            >
              Assessments
            </button>
          </>
        )}

        {/* COMMON */}
        <button className="logout-btn" onClick={logout}>
          Logout
        </button>

      </div>

      {/* HELP CARD */}
      <div className="help-section">
        <h4>Need Help?</h4>
        <p>If you are feeling distressed or in crisis, please reach out.</p>
        <button className="support-btn">Get Support</button>
      </div>

    </div>
  );
}