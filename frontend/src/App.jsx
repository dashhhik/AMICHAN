import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import BoardList from "./components/BoardList";
import BoardThreads from "./components/BoardThreads";
import MagicLinkAuth from "./components/MagicLinkAuth";
import VerifyMagicLink from "./components/VerifyMagicLink";
import RequireAuth from "./components/RequireAuth";

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
            </Routes>
        </Router>
    );
}

export default App;
