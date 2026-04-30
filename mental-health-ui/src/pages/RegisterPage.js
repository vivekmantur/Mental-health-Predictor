import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css"; // reuse same style

import {
  requestRegisterOtp,
  registerUser
} from "../api/authapi";

export default function RegisterPage() {
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSent, setOtpSent] = useState(false);
  const [loading, setLoading] = useState(false);

  // STEP 1: Request OTP
  const handleGetOtp = async () => {
    try {
      setLoading(true);
      await requestRegisterOtp(phone, email);
      setOtpSent(true);
      alert("OTP sent to your email");
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  // STEP 2: Verify OTP + Register
  const handleRegister = async () => {
    try {
      setLoading(true);

      const res = await registerUser(phone, email, otp);

      // store token + user
      sessionStorage.setItem("token", res.access_token);
      sessionStorage.setItem("user", JSON.stringify(res.user));

      alert("Registration successful!");

      navigate("/my-assessments");

    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">

        <h2 className="login-title">Register</h2>

        {!otpSent ? (
          <>
            <input
              type="text"
              placeholder="Enter phone number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              className="login-input"
            />

            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="login-input"
            />

            <button
              className="login-btn-primary"
              onClick={handleGetOtp}
              disabled={loading}
            >
              {loading ? "Sending..." : "Get OTP"}
            </button>
          </>
        ) : (
          <>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="login-input"
            />

            <button
              className="login-btn-primary"
              onClick={handleRegister}
              disabled={loading}
            >
              {loading ? "Verifying..." : "Verify & Register"}
            </button>
          </>
        )}

        <p className="login-footer">
          Already have an account?{" "}
          <span onClick={() => navigate("/login")}>Login</span>
        </p>

      </div>
    </div>
  );
}