import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../services/api"; // Используем api.js
import "../styles/AdminPostsList.css";

const AdminPostsList = () => {
    const { thread_id } = useParams(); // Получаем thread_id из URL
    const navigate = useNavigate();
    const [thread, setThread] = useState(null);
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchPosts();
    }, [thread_id]);

    const fetchPosts = async () => {
        setLoading(true);
        setError(""); // Сброс ошибок
        try {
            const response = await api.get(`/thread/${thread_id}`); // Эндпоинт для получения треда и постов
            setThread(response.data.thread);
            setPosts(response.data.posts);
        } catch (err) {
            console.error(err);
            setError("Ошибка при загрузке данных постов.");
        } finally {
            setLoading(false);
        }
    };

    const handleDeletePost = async (postId) => {
        const confirmDelete = window.confirm("Вы уверены, что хотите удалить этот пост?");
        if (!confirmDelete) return;

        try {
            await api.delete(`/post/${postId}`);
            alert("Пост успешно удален!");
            fetchPosts(); // Обновляем список постов после удаления
        } catch (err) {
            console.error(err);
            alert("Ошибка при удалении поста.");
        }
    };

    if (loading) {
        return (
            <div className="admin-posts-list-container">
                <p>Загрузка...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="admin-posts-list-container">
                <p className="error-message">{error}</p>
            </div>
        );
    }

    return (
        <div className="admin-posts-list-container">
            <button onClick={() => navigate(-1)} className="back-button">
                Назад
            </button>
            {thread && (
                <>
                    <h1>{thread.title}</h1>
                    <p>{thread.content}</p>
                    <small>Автор: {thread.nickname}</small>
                </>
            )}
            <hr />
            <h2>Посты</h2>
            {posts.length === 0 ? (
                <p>Посты отсутствуют.</p>
            ) : (
                <ul className="admin-posts-list">
                    {posts.map((post) => (
                        <li key={post.id} className="admin-post-item">
                            <div className="post-info">
                                <p>{post.content}</p>
                                <small>Автор: {post.nickname}</small>
                                <small>Создано: {new Date(post.created_at).toLocaleString()}</small>
                            </div>
                            <button
                                onClick={() => handleDeletePost(post.id)}
                                className="delete-post-button"
                            >
                                Удалить
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default AdminPostsList;
