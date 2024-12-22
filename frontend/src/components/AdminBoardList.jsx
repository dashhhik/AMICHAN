import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api"; // Используем api.js
import "../styles/AdminBoardList.css";

const AdminBoardList = () => {
    const [boards, setBoards] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchBoards();
    }, []);

    const fetchBoards = async () => {
        setLoading(true);
        try {
            const response = await api.get("/board"); // Эндпоинт для получения списка досок
            setBoards(response.data.boards);
        } catch (err) {
            console.error(err);
            setError("Ошибка при загрузке досок.");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (boardId) => {
        const confirmDelete = window.confirm("Вы уверены, что хотите удалить эту доску?");
        if (!confirmDelete) return;

        try {
            await api.delete(`/board/${boardId}`);
            alert("Доска успешно удалена!");
            fetchBoards(); // Обновляем список после удаления
        } catch (err) {
            console.error(err);
            alert("Ошибка при удалении доски.");
        }
    };

    const handleNavigateToThreads = (boardId) => {
        navigate(`/admin/${boardId}/threads`); // Редирект на страницу тредов доски
    };

    const handleNavigateToCreateBoard = () => {
        navigate("/admin/create-board"); // Редирект на страницу создания борда
    };

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="admin-board-list-container">
            <div className="header">
                <h1>Административная панель: Список досок</h1>
                <button className="create-board-button" onClick={handleNavigateToCreateBoard}>
                    Создать доску
                </button>
            </div>
            <ul className="admin-board-list">
                {boards.map((board) => (
                    <li key={board.id} className="admin-board-item">
                        <div className="board-info">
                            <h2>{board.name}</h2>
                            <p>{board.description}</p>
                        </div>
                        <div className="board-actions">
                            <button
                                onClick={() => handleNavigateToThreads(board.id)}
                                className="view-threads-button"
                            >
                                Перейти к тредам
                            </button>
                            <button
                                onClick={() => handleDelete(board.id)}
                                className="delete-board-button"
                            >
                                Удалить
                            </button>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AdminBoardList;
