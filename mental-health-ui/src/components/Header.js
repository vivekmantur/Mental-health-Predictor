import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/header.css";
import logo from "../assets/cognine-transparent.png";

export default function Header() {
  const navigate = useNavigate();

  // ✅ ALWAYS GET LATEST USER
  const user = sessionStorage.getItem("user");

  const handleLogout = () => {
    sessionStorage.removeItem("token");
    sessionStorage.removeItem("user");
    navigate("/login");
  };

  return (
    <header className="header-glass">
      <div className="header-container">

        {/* LEFT LOGO */}
        <button
          type="button"
          className="brand-lockup"
          onClick={() => navigate("/")}
        >
          <span className="logo-stage">
            <img src={logo} alt="Cognine" />
          </span>
        </button>

        {/* RIGHT SIDE */}
        <div className="header-actions">

          {user ? (
            <>
              <span className="user-email">{user.email}</span>
              <button className="logout-btn" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <>
              <button onClick={() => navigate("/login")} className="login-btn">
                Login
              </button>
              <button onClick={() => navigate("/register")} className="register-btn">
                Register
              </button>
            </>
          )}

        </div>
      </div>
    </header>
  );
}