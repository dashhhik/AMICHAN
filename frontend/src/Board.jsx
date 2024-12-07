import React, { useState, useEffect } from "react";
import { getBoardThreads, postBoardMessage } from "./api";

const BoardThreads = ({ boardId }) => {
  const [threads, setThreads] = useState([]); 
  const [newThread, setNewThread] = useState({
    title: "",
    content: "",
    nickname: "",
  }); 
  const [loading, setLoading] = useState(false); 


  useEffect(() => {
    loadThreads();
  }, [boardId]);

  const loadThreads = async () => {
    setLoading(true);
    try {
      const data = await getBoardThreads(boardId);
      setThreads(data.threads || []);
    } catch (err) {
      console.error("Error loading threads:", err);
    } finally {
      setLoading(false);
    }
  };


  const handleCreateThread = async (e) => {
    e.preventDefault();
    const payload = {
      thread: {
        board_id: boardId,
        title: newThread.title,
        content: newThread.content,
        created_at: new Date().toISOString(),
        nickname: newThread.nickname,
      },
    };
    try {
      await postBoardMessage(boardId, payload);
      setNewThread({ title: "", content: "", nickname: "" });
      loadThreads(); 
    } catch (err) {
      console.error("Error creating thread:", err);
    }
  };

  return (
    <div>
      <h1>Threads on Board {boardId}</h1>

      {loading && <p>Loading...</p>}
      <ul>
        {threads.map((thread, index) => (
          <li key={index} style={{ marginBottom: "20px" }}>
            <h3>{thread.title}</h3>
            <p>{thread.content}</p>
            <small>
              By <strong>{thread.nickname}</strong> at{" "}
              {new Date(thread.created_at).toLocaleString()}
            </small>
            <p>Replies: {thread.replies_count}</p>
          </li>
        ))}
      </ul>

      <form onSubmit={handleCreateThread} style={{ marginTop: "20px" }}>
        <h2>Create a New Thread</h2>
        <div>
          <label>Nickname:</label>
          <input
            type="text"
            value={newThread.nickname}
            onChange={(e) =>
              setNewThread({ ...newThread, nickname: e.target.value })
            }
            required
          />
        </div>
        <div>
          <label>Title:</label>
          <input
            type="text"
            value={newThread.title}
            onChange={(e) =>
              setNewThread({ ...newThread, title: e.target.value })
            }
            required
          />
        </div>
        <div>
          <label>Content:</label>
          <textarea
            value={newThread.content}
            onChange={(e) =>
              setNewThread({ ...newThread, content: e.target.value })
            }
            required
          />
        </div>
        <button type="submit">Create Thread</button>
      </form>
    </div>
  );
};

export default BoardThreads;