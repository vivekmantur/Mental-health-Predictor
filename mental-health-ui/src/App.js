import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import AssessmentPage from "./pages/AssessmentPage";

import Header from "./components/Header";
import Footer from "./components/Footer";

import "./styles/layout.css";

function Layout() {
  const location = useLocation();

  // ✅ SHOW HEADER EVERYWHERE
  const hideHeaderRoutes = [];
  const isHidden = hideHeaderRoutes.includes(location.pathname);

  return (
    <div className="app-bg">

      {/* ✅ HEADER ALWAYS VISIBLE */}
      {!isHidden && <Header />}

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/assessment" element={<AssessmentPage />} />
      </Routes>

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