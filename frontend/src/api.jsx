import axios from "axios"

const api = axios.create({
    baseURL:  "http://localhost:8000",
});

export const getBoards = async () => {
    const response = await api.get("/board/");
    return response.data;
}

export const getBoardThreads = async (boardId) => {
    const response = await api.get(`/board/${boardId}/threads`);
    return response.data;
}

export const postBoardMessage = async (boardId, payload) => {
    const response = await api.post(`/board/${boardId}/threads`, payload);
    return response.data;
  };
  export default api;