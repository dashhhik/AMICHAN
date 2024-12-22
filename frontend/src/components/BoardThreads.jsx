import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/BoardThreads.css";

const BoardThreads = () => {
    const { boardId } = useParams();
    const navigate = useNavigate();
    const [threads, setThreads] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [newThreadTitle, setNewThreadTitle] = useState(""); // Заголовок нового треда
    const [newThreadContent, setNewThreadContent] = useState(""); // Содержимое нового треда
    const [newThreadNickname, setNewThreadNickname] = useState(""); // Никнейм (опционально)
    const token = localStorage.getItem("jwtToken"); // JWT токен для авторизации

    useEffect(() => {
        api
            .get(`http://0.0.0.0:8000/board/${boardId}/threads`, {
                headers: { accept: "application/json" },
            })
            .then((response) => {
                console.log("Полученные треды:", response.data.threads); // Проверка данных
                setThreads(response.data.threads);
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setError("Ошибка при загрузке данных.");
                setLoading(false);
            });
    }, [boardId]);

    const handleNavigateToPosts = (threadId) => {
        console.log("Переданный threadId:", threadId); // Проверка threadId
        if (!threadId) {
            console.error("ID треда не определен!");
            return;
        }
        navigate(`/thread/${threadId}`);
    };

    const handleCreateThread = () => {
        if (!token) {
            alert("Вы не авторизованы. Пожалуйста, войдите в систему.");
            return;
        }

        if (!newThreadTitle.trim() || !newThreadContent.trim()) {
            alert("Все поля должны быть заполнены.");
            return;
        }

        api
            .post(
                `http://0.0.0.0:8000/board/${boardId}/threads`,
                {
                    thread: {
                        title: newThreadTitle,
                        content: newThreadContent,
                        nickname: newThreadNickname || null, // Никнейм, если не указан, будет null
                    },
                },
                {
                    headers: {
                        Authorization: `Token ${token}`,
                        "Content-Type": "application/json",
                    },
                }
            )
            .then((response) => {
                alert("Тред успешно создан!");
                const newThread = response.data.thread; // Извлекаем тред из респонса
                setThreads([...threads, newThread]); // Добавляем новый тред в список
                setNewThreadTitle(""); // Очищаем поля
                setNewThreadContent("");
                setNewThreadNickname("");
            })
            .catch((err) => {
                console.error(err);
                alert("Ошибка при создании треда.");
            });
    };

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="threads-container">
            <h1 className="board-header">Треды для доски #{boardId}</h1>

            {/* Форма для создания нового треда */}
            <div className="new-thread-form">
                <h2>Создать новый тред</h2>
                <input
                    type="text"
                    placeholder="Заголовок"
                    value={newThreadTitle}
                    onChange={(e) => setNewThreadTitle(e.target.value)}
                    className="new-thread-title"
                />
                <textarea
                    placeholder="Содержимое"
                    value={newThreadContent}
                    onChange={(e) => setNewThreadContent(e.target.value)}
                    className="new-thread-content"
                />
                <input
                    type="text"
                    placeholder="Никнейм (опционально)"
                    value={newThreadNickname}
                    onChange={(e) => setNewThreadNickname(e.target.value)}
                    className="new-thread-nickname"
                />
                <button onClick={handleCreateThread} className="create-thread-button">
                    Создать тред
                </button>
            </div>

            {/* Список тредов */}
            {threads.map((thread) => (
                <div key={thread.id} className="thread-item">
                    <div className="thread-header">
                        <span className="thread-date">
                            {new Date(thread.created_at).toLocaleString()}
                        </span>
                        <span className="thread-id">ID: {thread.id}</span>
                    </div>
                    <h2 className="thread-title">{thread.title}</h2>
                    <p className="thread-content">{thread.content}</p>
                    <p className="thread-nickname">
                        Автор: {thread.nickname || "Аноним"}
                    </p>
                    <button onClick={() => handleNavigateToPosts(thread.id)}>
                        Перейти к постам
                    </button>
                </div>
            ))}
        </div>
    );
};

export default BoardThreads;
