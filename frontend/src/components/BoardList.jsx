import React, { useEffect, useState } from "react";
import { fetchBoards } from "../services/boardService";
import "../styles/BoardList.css";

const BoardList = () => {
    const [boards, setBoards] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchBoards()
            .then((data) => {
                setBoards(data.boards);
                setLoading(false);
            })
            .catch((err) => {
                console.error(err);
                setError("Ошибка при загрузке данных.");
                setLoading(false);
            });
    }, []);

    if (loading) return <p>Загрузка...</p>;
    if (error) return <p>{error}</p>;

    // Группировка досок по колонкам (например, 4 колонки)
    const columns = [[], [], [], []];
    boards.forEach((board, index) => {
        columns[index % 4].push(board);
    });

    return (
        <div className="board-container">
            <h1 className="board-header">Доски</h1>
            <div className="board-grid">
                {columns.map((column, colIndex) => (
                    <div key={colIndex} className="board-column">
                        {column.map((board) => (
                            <div key={board.id} className="board-item">
                                <a href={`/board/${board.id}`} className="board-link">
                                    {board.name}
                                </a>
                            </div>
                        ))}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BoardList;
