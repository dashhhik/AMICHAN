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
import ThreadPosts from "./components/ThreadPosts";
import AdminPostList from "./components/AdminPostList";

function App() {
    return (
        <Router>
            <Routes>
                {/* Публичные маршруты, не требующие аутентификации */}
                <Route path="/auth" element={<MagicLinkAuth />} />
                <Route path="/auth/verify_magic_link/:token" element={<VerifyMagicLink />} />

                {/* Маршруты, защищенные аутентификацией */}
                <Route
                    path="*"
                    element={
                        <RequireAuth>
                            <Routes>
                                <Route path="/" element={<BoardList />} />
                                <Route path="/board/:boardId" element={<BoardThreads />} />
                                <Route path="/admin/login" element={<LoginForm />} />
                                <Route path="/admin/create-board" element={<CreateBoard />} />
                                <Route path="/admin/boards" element={<AdminBoardList />} />
                                <Route path="/admin/:board_id/threads" element={<AdminThreadList />} />
                                <Route path="/admin/thread/:thread_id/posts" element={<AdminPostList />} />
                                <Route path="/thread/:threadId" element={<ThreadPosts />} />
                            </Routes>
                        </RequireAuth>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
