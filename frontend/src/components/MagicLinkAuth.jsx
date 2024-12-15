import React, { useState } from "react";
import axios from "axios";
import "../styles/MagicLinkAuth.css"; // Подключаем CSS-файл

const MagicLinkAuth = () => {
    const [email, setEmail] = useState(""); // Состояние для хранения email
    const [message, setMessage] = useState(""); // Сообщение об успехе или ошибке
    const [loading, setLoading] = useState(false);

    const handleSendMagicLink = async () => {
        setMessage(""); // Очистка сообщений
        setLoading(true);

        try {
            // Отправка POST-запроса
            const response = await axios.post("http://0.0.0.0:8000/auth/send_magic_link/", {
                email: email,
            });

            // Успешное выполнение
            setMessage("Magic link отправлен на вашу почту!");
        } catch (error) {
            console.error(error);
            setMessage("Ошибка при отправке magic link. Проверьте email.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <h1>Аутентификация через Magic Link</h1>
            <p>Введите вашу электронную почту, чтобы получить magic link:</p>
            <input
                type="email"
                placeholder="user@edu.hse.ru"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="auth-input"
            />
            <br />
            <button
                onClick={handleSendMagicLink}
                className="auth-button"
                disabled={loading}
            >
                {loading ? "Отправка..." : "Отправить Magic Link"}
            </button>
            {message && <p className="auth-message">{message}</p>}
        </div>
    );
};

export default MagicLinkAuth;
