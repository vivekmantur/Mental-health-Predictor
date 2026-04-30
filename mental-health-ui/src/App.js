import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import AssessmentPage from "./pages/AssessmentPage";
import DoctorDashboard from "./pages/DoctorDashboard";
import MyAssessmentsPage from "./pages/MyAssessmentsPage";
import AssessmentsListPage from "./pages/AssessmentsListPage";

import Header from "./components/Header";
import Footer from "./components/Footer";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProtectedRoute from "./components/ProtectedRoute";

import "./styles/layout.css";

function Layout() {
  const location = useLocation();

  // 🔥 Routes where header should NOT appear
  const hideHeaderRoutes = [
    "/login",
    "/register",
    "/my-assessments",
    "/assessments",
    "/doctor",
    "/assessment",
  ];

  const hideHeader = hideHeaderRoutes.includes(location.pathname);

  return (
    <div className="app-bg">

      {/* ✅ HEADER */}
      {!hideHeader && <Header />}

      {/* ✅ MAIN CONTENT WRAPPER (IMPORTANT FIX) */}
      <div className="app-content">
        <Routes>

          {/* 🔓 Public Routes */}
          <Route path="/" element={<Dashboard />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />

          {/* 🔐 Protected Routes */}

          <Route
            path="/assessment"
            element={
              <ProtectedRoute allowedRole="patient">
                <AssessmentPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/doctor"
            element={
              <ProtectedRoute allowedRole="doctor">
                <DoctorDashboard />
              </ProtectedRoute>
            }
          />

          <Route
            path="/my-assessments"
            element={
              <ProtectedRoute allowedRole="patient">
                <MyAssessmentsPage />
              </ProtectedRoute>
            }
          />

          <Route
            path="/assessments"
            element={
              <ProtectedRoute allowedRole="patient">
                <AssessmentsListPage />
              </ProtectedRoute>
            }
          />

        </Routes>
      </div>

      {/* ✅ FOOTER */}
      <Footer />

    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

export default App;