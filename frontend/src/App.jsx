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
import AdminDashboard from "./components/AdminDashboard.jsx";

function App() {
    return (
        <Router>
            <Routes>
                {/* Публичные маршруты, не требующие аутентификации */}
                <Route path="/auth" element={<MagicLinkAuth />} />
                <Route path="/auth/verify_magic_link/:token" element={<VerifyMagicLink />} />

                {/* Защищенные маршруты */}
                <Route
                    path="/"
                    element={
                        <RequireAuth>
                            <BoardList />
                        </RequireAuth>
                    }
                />
                <Route
                    path="/board/:boardId"
                    element={
                        <RequireAuth>
                            <BoardThreads />
                        </RequireAuth>
                    }
                />
                <Route
                    path="/thread/:threadId"
                    element={
                        <RequireAuth>
                            <ThreadPosts />
                        </RequireAuth>
                    }
                />

                {/* Административные маршруты */}
                <Route path="/admin" element={<AdminDashboard />}>
                    <Route path="login" element={<LoginForm />} />
                    <Route path="create-board" element={<CreateBoard />} />
                    <Route path="boards" element={<AdminBoardList />} />
                    <Route path=":board_id/threads" element={<AdminThreadList />} />
                    <Route path="threads/:thread_id/posts" element={<AdminPostList />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;
