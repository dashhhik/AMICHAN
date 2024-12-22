import React from "react";
import { Outlet, Link } from "react-router-dom";
import "../styles/AdminDashboard.css";

const AdminDashboard = () => {
    return (
        <div className="admin-dashboard">
            <nav className="admin-sidebar">
                <ul>
                    <li>
                        <Link to="/admin/boards">Список досок</Link>
                    </li>
                    <li>
                        <Link to="/admin/create-board">Создать доску</Link>
                    </li>
                    <li>
                        <Link to="/admin/login">Логин</Link>
                    </li>
                </ul>
            </nav>
            <div className="admin-content">
                <Outlet />
            </div>
        </div>
    );
};

export default AdminDashboard;
