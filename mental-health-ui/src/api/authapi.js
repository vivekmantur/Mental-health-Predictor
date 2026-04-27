import { buildApiUrl } from "./baseUrl";

const BASE = buildApiUrl();

async function handleResponse(res, defaultMsg) {
  if (res.ok) return res.json();

  let msg = defaultMsg;
  try {
    const data = await res.json();
    msg = data.detail || defaultMsg;
  } catch {}

  throw new Error(msg);
}

// ================= LOGIN =================
export async function requestOtp(phone) {
  const res = await fetch(`${BASE}/api/v1/auth/request-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone }),
  });

  return handleResponse(res, "User not found");
}

export async function verifyOtp(phone, otp) {
  const res = await fetch(`${BASE}/api/v1/auth/verify-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, otp }),
  });

  return handleResponse(res, "Invalid OTP");
}

// ================= REGISTER =================

// STEP 1 → Send OTP
export async function requestRegisterOtp(phone, email) {
  const res = await fetch(`${BASE}/api/v1/auth/register-otp`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, email }),
  });

  return handleResponse(res, "User already exists");
}

// STEP 2 → Verify OTP & Create User
export async function registerUser(phone, email, otp) {
  const res = await fetch(`${BASE}/api/v1/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, email, otp }),
  });

  return handleResponse(res, "Registration failed");
}