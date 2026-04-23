
// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import Navbar from "./components/Navbar";
// import Home from "./pages/Home";
// import RegisterAsset from "./pages/RegisterAsset";
// import DetectLeak from "./pages/DetectLeak";
// import RiskMonitor from "./pages/RiskMonitor";

// function App() {
//   return (
//     <Router>
//       {/* ✅ Navbar always visible */}
//       <Navbar />

//       {/* ✅ Page Routes */}
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/register" element={<RegisterAsset />} />
//         <Route path="/detect" element={<DetectLeak />} />
//         <Route path="/risk" element={<RiskMonitor />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;

// import React from "react";
// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// import Navbar from "./components/Navbar";
// import Home from "./pages/Home";
// import RegisterAsset from "./pages/RegisterAsset";
// import DetectLeak from "./pages/DetectLeak";
// import Honeypot from "./pages/Honeypot";     // ⭐ ADDED
// import RiskMonitor from "./pages/RiskMonitor";

// function App() {
//   return (
//     <Router>
//       {/* Navbar */}
//       <Navbar />

//       {/* Routes */}
//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/register" element={<RegisterAsset />} />
//         <Route path="/detect" element={<DetectLeak />} />
//         <Route path="/honeypot" element={<Honeypot />} /> {/* ⭐ ADDED */}
//         <Route path="/risk" element={<RiskMonitor />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;

import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import RegisterAsset from "./pages/RegisterAsset";
import DetectLeak from "./pages/DetectLeak";
import Honeypot from "./pages/Honeypot";
import RiskMonitor from "./pages/RiskMonitor";

function App() {
  return (
    <Router>
      {/* Navbar */}
      <Navbar />

      {/* ✅ MAIN LAYOUT WRAPPER (IMPORTANT) */}
      <div className="page-wrapper">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/register" element={<RegisterAsset />} />
          <Route path="/detect" element={<DetectLeak />} />
          <Route path="/honeypot" element={<Honeypot />} />
          <Route path="/risk" element={<RiskMonitor />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;