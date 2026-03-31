import React from "react";
import "../styles/layout.css";

export default function Footer() {
  return (
    <div className="footer">
      <div className="footer-inner">   {/* ✅ THIS WAS MISSING */}
        <p>© 2026 Mental Health AI Platform</p>
      </div>
    </div>
  );
}