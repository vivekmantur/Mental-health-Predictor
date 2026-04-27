import { buildApiUrl } from "./baseUrl";

const BASE = buildApiUrl();

export async function getPatients() {
  const token = sessionStorage.getItem("token");

  const res = await fetch(`${BASE}/api/v1/doctor/patients`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });

  if (!res.ok) throw new Error("Failed to fetch patients");

  return res.json();
}

// ✅ FIXED (correct endpoint + clean)
export async function updateAssessment(id, payload) {
  const token = sessionStorage.getItem("token");

  const res = await fetch(
    `${BASE}/api/v1/doctor/assessments/${id}`,   // ✅ FIXED
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify(payload)
    }
  );

  if (!res.ok) throw new Error("Update failed");

  return res.json();
}

// ✅ STATUS UPDATE
export async function updateAssessmentStatus(id, status) {
  const token = sessionStorage.getItem("token");

  const res = await fetch(
    `${BASE}/api/v1/doctor/assessments/${id}/status`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ status })
    }
  );

  if (!res.ok) throw new Error("Status update failed");

  return res.json();
}