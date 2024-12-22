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

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="threads-container">
            <h1 className="board-header">Треды для доски #{boardId}</h1>
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
                    <button onClick={() => handleNavigateToPosts(thread.id)}>
                        Перейти к постам
                    </button>
                </div>
            ))}
        </div>
    );
};

export default BoardThreads;
