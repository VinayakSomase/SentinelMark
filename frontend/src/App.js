import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import RegisterAsset from "./pages/RegisterAsset";
import DetectLeak from "./pages/DetectLeak";
const API = "http://127.0.0.1:8000";
function App() {
  return (
    <Router>
      <Navbar />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register" element={<RegisterAsset />} />
        <Route path="/detect" element={<DetectLeak />} />
      </Routes>

    </Router>
  );
}

export default App;