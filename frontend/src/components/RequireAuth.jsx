import React from "react";
import { Navigate } from "react-router-dom";

const RequireAuth = ({ children }) => {
    const token = localStorage.getItem("jwtToken");

    if (!token) {
        // Перенаправляем на страницу аутентификации, если токена нет
        return <Navigate to="/auth" replace />;
    }

    return children;
};

export default RequireAuth;
