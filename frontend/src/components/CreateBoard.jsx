import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; // Используем api.js
import "../styles/CreateBoard.css";

const CreateBoard = () => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        try {
            // Отправка POST-запроса
            const response = await api.post("/board/", {
                name,
                description,
            });

            alert(response.data.message); // Показываем сообщение об успехе
            navigate("/"); // Перенаправляем на главную страницу
        } catch (err) {
            console.error(err);
            const errorMessage = err.response?.data?.detail || "Ошибка при создании доски.";
            setError(errorMessage);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="create-board-container">
            <h1>Создать новую доску</h1>
            <form onSubmit={handleSubmit} className="create-board-form">
                {error && <p className="error-message">{error}</p>}
                <div className="form-group">
                    <label htmlFor="name">Название доски</label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Введите название доски"
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="description">Описание доски</label>
                    <textarea
                        id="description"
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Введите описание доски"
                        required
                    />
                </div>
                <button type="submit" className="submit-button" disabled={loading}>
                    {loading ? "Создание..." : "Создать"}
                </button>
            </form>
        </div>
    );
};

export default CreateBoard;
