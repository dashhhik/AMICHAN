import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api"; // Используем api.js
import "../styles/AdminThreadList.css";

const AdminThreadList = () => {
    const { board_id } = useParams(); // Получаем board_id из URL
    const navigate = useNavigate();
    const [threads, setThreads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchThreads();
    }, [board_id]);

    const fetchThreads = async () => {
        setLoading(true);
        setError(""); // Сброс ошибки
        try {
            const response = await api.get(`/board/${board_id}/threads`); // Получение тредов по board_id
            setThreads(response.data.threads);
        } catch (err) {
            console.error(err);
            setError("Ошибка при загрузке тредов.");
        } finally {
            setLoading(false);
        }
    };

    const handleNavigateToPosts = (threadId) => {
        // Перенаправляем на страницу, где будут отображаться посты, связанные с тредом
        navigate(`/admin/threads/${threadId}/posts`);
    };

    const handleDelete = async (threadId) => {
        const confirmDelete = window.confirm("Вы уверены, что хотите удалить этот тред?");
        if (!confirmDelete) return;

        try {
            await api.delete(`/thread/${threadId}`);
            alert("Тред успешно удален!");
            fetchThreads(); // Обновляем список после удаления
        } catch (err) {
            console.error(err);
            alert("Ошибка при удалении треда.");
        }
    };

    if (loading) {
        return (
            <div className="admin-thread-list-container">
                <p>Загрузка...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="admin-thread-list-container">
                <p className="error-message">{error}</p>
            </div>
        );
    }

    return (
        <div className="admin-thread-list-container">
            <h1>Треды для доски #{board_id}</h1>
            {threads.length === 0 ? (
                <p>Треды отсутствуют.</p>
            ) : (
                <ul className="admin-thread-list">
                    {threads.map((thread) => (
                        <li key={thread.id} className="admin-thread-item">
                            <div className="thread-info">
                                <h2>{thread.title}</h2>
                                <p>{thread.content}</p>
                                <small>Автор: {thread.nickname}</small>
                            </div>
                            <div className="thread-actions">
                                <button
                                    onClick={() => handleNavigateToPosts(thread.id)}
                                    className="view-posts-button"
                                >
                                    Перейти к постам
                                </button>
                                <button
                                    onClick={() => handleDelete(thread.id)}
                                    className="delete-thread-button"
                                >
                                    Удалить
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default AdminThreadList;
