import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import BoardList from "./components/BoardList";
import BoardThreads from "./components/BoardThreads";
import MagicLinkAuth from "./components/MagicLinkAuth";
import VerifyMagicLink from "./components/VerifyMagicLink";
import RequireAuth from "./components/RequireAuth";
import LoginForm from "./components/Login.jsx";
import CreateBoard from "./components/CreateBoard.jsx";
import AdminBoardList from "./components/AdminBoardList.jsx";
import AdminThreadList from "./components/AdminThreadList.jsx";
import AdminPostList from "./components/AdminPostList.jsx";
import ThreadPosts from "./components/AdminPostList.jsx";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<BoardList />} />
                <Route path="/auth" element={<MagicLinkAuth />} />
                <Route path="/auth/verify_magic_link/:token" element={<VerifyMagicLink />} />
                <Route
                    path="/board/:boardId"
                    element={
                        <RequireAuth>
                            <BoardThreads />
                        </RequireAuth>
                    }
                />
                <Route path="/admin/login" element={<LoginForm />} />
                <Route path="/admin/create-board" element={<CreateBoard />} />
                <Route path="/admin/boards" element={<AdminBoardList />} />
                <Route path="/admin/:board_id/threads" element={<AdminThreadList />} />
                {/*<Route path="/admin/:board_id/threads" element={<AdminThreadList />} />*/}
                <Route path="/admin/thread/:thread_id/posts" element={<AdminPostList />} />
            </Routes>
        </Router>
    );
}

export default App;
