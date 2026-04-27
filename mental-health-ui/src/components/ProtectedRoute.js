import { Navigate } from "react-router-dom";

const ProtectedRoute = ({ children, allowedRole }) => {
  const token = sessionStorage.getItem("token");
  const user = JSON.parse(sessionStorage.getItem("user"));

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // 🔥 Prevent undefined role issues
  if (!allowedRole) {
    console.error("ProtectedRoute missing allowedRole!");
    return children;
  }

  if (user?.usertype !== allowedRole) {
    if (user?.usertype === "doctor") {
      return <Navigate to="/doctor" replace />;
    } else {
      return <Navigate to="/my-assessments" replace />;
    }
  }

  return children;
};

export default ProtectedRoute;