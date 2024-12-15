import axios from "axios";

export const fetchBoards = async () => {
    const response = await axios.get("http://0.0.0.0:8000/board/", {
        headers: { accept: "application/json" },
    });
    return response.data;
};
