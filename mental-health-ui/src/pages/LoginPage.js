import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { requestOtp, verifyOtp } from "../api/authapi";
import "../styles/login.css";

export default function LoginPage() {
  const navigate = useNavigate();

  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // 🔥 Auto redirect if already logged in
  useEffect(() => {
    const token = sessionStorage.getItem("token");

    if (token) {
      const user = JSON.parse(sessionStorage.getItem("user"));

      if (user?.usertype === "doctor") {
        navigate("/doctor", { replace: true });
      } else {
        navigate("/my-assessments", { replace: true });
      }
    }
  }, [navigate]);

  // 🔹 Request OTP
  const handleRequestOtp = async () => {
    if (!phone) {
      alert("Please enter phone number");
      return;
    }

    try {
      setLoading(true);
      await requestOtp(phone);
      setStep(2);
    } catch (error) {
      alert(error.message || "Failed to send OTP");
    } finally {
      setLoading(false);
    }
  };

  // 🔹 Verify OTP
  const handleVerifyOtp = async () => {
    if (!otp) {
      alert("Please enter OTP");
      return;
    }

    try {
      setLoading(true);

      const res = await verifyOtp(phone, otp);
      const user = res.user;

      // ✅ Store token
      sessionStorage.setItem("token", res.access_token);

      // ✅ Store full user object
      sessionStorage.setItem("user", JSON.stringify(user));

      // ✅ 🔥 Store email (IMPORTANT FIX)
      const email = user?.email || `${phone}@user.com`; // fallback if email not present
      sessionStorage.setItem("email", email);

      // ✅ Redirect based on role
      if (user?.usertype === "doctor") {
        navigate("/doctor", { replace: true });
      } else {
        navigate("/my-assessments", { replace: true });
      }

    } catch (error) {
      alert(error.message || "Invalid OTP");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">

        <h2 className="login-title">Login</h2>

        {step === 1 && (
          <>
            <input
              className="login-input"
              placeholder="Enter phone number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />

            <button
              className="login-btn"
              onClick={handleRequestOtp}
              disabled={loading}
            >
              {loading ? "Sending..." : "Get OTP"}
            </button>
          </>
        )}

        {step === 2 && (
          <>
            <input
              className="login-input"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />

            <button
              className="login-btn"
              onClick={handleVerifyOtp}
              disabled={loading}
            >
              {loading ? "Verifying..." : "Verify OTP"}
            </button>
          </>
        )}

        <div className="login-note">
          Secure OTP-based login
        </div>

      </div>
    </div>
  );
} 