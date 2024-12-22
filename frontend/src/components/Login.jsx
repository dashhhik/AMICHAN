import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api.jsx"; // Используем api.js для запросов
import "../styles/LoginForm.css";

const LoginForm = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            const response = await api.post("/login", {
                email,
                password,
            });
            const { token } = response.data;

            // Сохраняем токен в localStorage
            localStorage.setItem("jwtToken", token);

            // Перенаправляем пользователя на главную страницу
            navigate("/");
        } catch (err) {
            console.error("Ошибка входа:", err);
            const errorMessage = err.response?.data?.detail || "Ошибка входа. Проверьте данные.";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <h1>Вход</h1>
            <form onSubmit={handleSubmit} className="login-form">
                {error && <p className="login-error">{error}</p>}
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Введите ваш email"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Пароль</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Введите ваш пароль"
                        required
                    />
                </div>
                <button type="submit" className="login-button" disabled={loading}>
                    {loading ? "Вход..." : "Войти"}
                </button>
            </form>
        </div>
    );
};

export default LoginForm;
