import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../services/api";
import "../styles/ThreadPosts.css";

const ThreadPosts = () => {
    const { threadId } = useParams();
    const [thread, setThread] = useState(null); // Данные о треде
    const [posts, setPosts] = useState([]); // Посты, связанные с тредом
    const [replyContent, setReplyContent] = useState(""); // Текст ответа
    const [loading, setLoading] = useState(true); // Индикатор загрузки
    const [error, setError] = useState(null); // Обработка ошибок
    const token = localStorage.getItem("jwtToken"); // JWT токен для авторизации

    // Загрузка данных треда и постов
    useEffect(() => {
        api
            .get(`http://0.0.0.0:8000/thread/${threadId}`, {
                headers: { accept: "application/json" },
            })
            .then((response) => {
                console.log("Полученные данные:", response.data);
                setThread(response.data.thread.thread); // Сохраняем данные о треде
                setPosts(response.data.posts); // Сохраняем посты
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setError("Ошибка при загрузке данных.");
                setLoading(false);
            });
    }, [threadId]);

    // Обработчик отправки ответа
    const handleReplySubmit = () => {
        if (!token) {
            alert("Вы не авторизованы. Пожалуйста, войдите в систему.");
            return;
        }

        if (!replyContent.trim()) {
            alert("Ответ не может быть пустым.");
            return;
        }

        api
            .post(
                `http://0.0.0.0:8000/post/${threadId}/reply`,
                {
                    content: replyContent,
                },
                {
                    headers: {
                        Authorization: `Token ${token}`,
                        "Content-Type": "application/json",
                    },
                }
            )
            .then((response) => {
                setReplyContent(""); // Очищаем поле ответа
                setPosts([...posts, response.data]); // Обновляем список постов
            })
            .catch((err) => {
                console.error(err);
                alert("Ошибка при отправке ответа.");
            });
    };

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p>{error}</p>;

    return (
        <div className="posts-container">
            {/* Информация о треде */}
            {thread && (
                <div className="thread-details">
                    <h1>{thread.title}</h1>
                    <p>{thread.content}</p>
                    <small>Автор: {thread.nickname || "Аноним"}</small>
                    <small>Дата создания: {new Date(thread.created_at).toLocaleString()}</small>
                    <small>Ответов: {thread.replies_count}</small>
                </div>
            )}
            <hr />
            {/* Форма для ответа */}
            <div className="reply-container">
                <textarea
                    className="reply-textarea"
                    placeholder="Введите ваш ответ здесь..."
                    value={replyContent}
                    onChange={(e) => setReplyContent(e.target.value)}
                />
                <button className="reply-button" onClick={handleReplySubmit}>
                    Отправить ответ
                </button>
            </div>
            <hr />
            {/* Посты */}
            <h2>Посты</h2>
            {posts.length === 0 ? (
                <p>Посты отсутствуют.</p>
            ) : (
                <ul className="post-list">
                    {posts.map((post) => (
                        <li key={post.id} className="post-item">
                            <p>{post.content}</p>
                            <small>Автор: {post.nickname || "Аноним"}</small>
                            <small>Дата: {new Date(post.created_at).toLocaleString()}</small>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ThreadPosts;
