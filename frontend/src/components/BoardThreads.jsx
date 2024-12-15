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
    const [replyContent, setReplyContent] = useState("");

    const token = localStorage.getItem("jwtToken");

    useEffect(() => {
        api
            .get(`http://0.0.0.0:8000/board/${boardId}/threads`, {
                headers: { accept: "application/json" },
            })
            .then((response) => {
                setThreads(response.data.threads);
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setError("Ошибка при загрузке данных.");
                setLoading(false);
            });
    }, [boardId]);

    const handleReply = (threadTitle) => {
        if (!token) {
            navigate("/auth");
            return;
        }

        if (!replyContent.trim()) {
            alert("Ответ не может быть пустым.");
            return;
        }

        api
            .post(
                `http://0.0.0.0:8000/board/${boardId}/threads`,
                {
                    thread: {
                        board_id: boardId,
                        title: threadTitle,
                        content: replyContent,
                        nickname: "Anonymous",
                    },
                },
                { headers: { Authorization: `Token ${token}` } }
            )
            .then(() => {
                alert("Ответ успешно добавлен!");
                setReplyContent("");
                return api.get(`http://0.0.0.0:8000/board/${boardId}/threads`);
            })
            .then((response) => setThreads(response.data.threads))
            .catch((err) => {
                console.error(err);
                alert(err.response?.data?.detail || "Ошибка при отправке ответа.");
            });
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
                    <textarea
                        className="reply-textarea"
                        placeholder="Введите ваш ответ здесь..."
                        value={replyContent}
                        onChange={(e) => setReplyContent(e.target.value)}
                    />
                    <button
                        className="reply-button"
                        onClick={() => handleReply(thread.title)}
                    >
                        Ответить
                    </button>
                </div>
            ))}
        </div>
    );
};

export default BoardThreads;
