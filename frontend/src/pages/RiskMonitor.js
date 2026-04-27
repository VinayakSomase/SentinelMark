
// import React, { useEffect, useState } from "react";
// import {
//   LineChart,
//   Line,
//   XAxis,
//   YAxis,
//   Tooltip,
//   ResponsiveContainer,
//   CartesianGrid,
// } from "recharts";

// function RiskMonitor() {
//   const [riskData, setRiskData] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");
//   const [filter, setFilter] = useState("all");
//   const [alert, setAlert] = useState("");

//   const fetchData = async () => {
//     try {
//       const res = await fetch("http://127.0.0.1:8000/api/risk-scores");
//       const data = await res.json();

//       setRiskData(data.risk_scores);
//       setError("");

//       if (data.risk_scores.some((d) => d.level === "high")) {
//         setAlert("⚠️ High Risk Distributor Detected!");
//       } else {
//         setAlert("");
//       }
//     } catch (err) {
//       setError("Failed to load data");
//     } finally {
//       setLoading(false);
//     }
//   };

//   useEffect(() => {
//     fetchData();
//     const interval = setInterval(fetchData, 5000);
//     return () => clearInterval(interval);
//   }, []);

//   const getColor = (level) => {
//     if (level === "high") return "#dc2626";   // red
//     if (level === "medium") return "#ca8a04"; // yellow
//     return "#16a34a";                         // green
//   };

//   const filteredData =
//     filter === "high"
//       ? riskData.filter((item) => item.level === "high")
//       : riskData;

//   if (loading) {
//     return (
//       <div style={{ color: "white", padding: "100px" }}>
//         <h2>Loading...</h2>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div style={{ color: "red", padding: "100px" }}>
//         <h2>{error}</h2>
//       </div>
//     );
//   }

//   return (
//     <div
//       style={{
//         padding: "100px 20px",
//         background: "#050816",
//         minHeight: "100vh",
//         color: "white",
//         fontFamily: "DM Sans, sans-serif",
//       }}
//     >
//       {/* HEADER */}
//       <h1 style={{ fontSize: "30px", marginBottom: "10px" }}>
//         Risk Monitoring
//       </h1>

//       <p style={{ color: "#9ca3af", marginBottom: "20px" }}>
//         Real-time distributor risk analysis and anomaly detection
//       </p>

//       {/* TIME */}
//       <p style={{ fontSize: "12px", color: "#6b7280", marginBottom: "10px" }}>
//         Last Updated: {new Date().toLocaleTimeString()}
//       </p>

//       {/* ALERT */}
//       {alert && (
//         <div
//           style={{
//             background: "#7f1d1d",
//             padding: "12px",
//             borderRadius: "8px",
//             marginBottom: "15px",
//             color: "#fecaca",
//             fontWeight: "600",
//             boxShadow: "0 0 10px rgba(220,38,38,0.4)",
//           }}
//         >
//           {alert}
//         </div>
//       )}

//       {/* HIGH RISK COUNT */}
//       <p style={{ marginBottom: "20px", color: "#ef4444", fontWeight: "600" }}>
//         High Risk Count: {riskData.filter((d) => d.level === "high").length}
//       </p>

//       {/* FILTER BUTTON */}
//       <button
//         onClick={() => setFilter(filter === "all" ? "high" : "all")}
//         style={{
//           marginBottom: "25px",
//           padding: "10px 18px",
//           borderRadius: "20px",
//           border: "none",
//           background: "#2563eb",
//           color: "white",
//           cursor: "pointer",
//           fontWeight: "600",
//         }}
//       >
//         {filter === "all" ? "Show High Risk Only" : "Show All"}
//       </button>

//       {/* 🔥 FIXED CHART */}
//       <div
//         style={{
//           background: "#111827",
//           padding: "20px",
//           borderRadius: "12px",
//           marginBottom: "30px",
//         }}
//       >
//         <h3 style={{ marginBottom: "15px" }}>Risk Overview</h3>

//         <ResponsiveContainer width="100%" height={280}>
//           <LineChart
//             data={riskData}
//             margin={{ top: 10, right: 10, left: 0, bottom: 10 }}
//           >
//             <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />

//             <XAxis
//               dataKey="name"
//               interval={0}
//               padding={{ left: 0, right: 0 }} // ⭐ FIXED alignment
//               tick={{ fill: "#9ca3af", fontSize: 11 }}
//             />

//             <YAxis
//               domain={[0, 100]}
//               tick={{ fill: "#9ca3af", fontSize: 11 }}
//             />

//             <Tooltip
//               contentStyle={{
//                 backgroundColor: "#111827",
//                 border: "1px solid #374151",
//                 color: "white",
//               }}
//             />

//             <Line
//               type="monotone"
//               dataKey="score"
//               stroke="#3b82f6"
//               strokeWidth={3}
//               dot={{ r: 5 }}
//               activeDot={{ r: 7 }}
//               animationDuration={1000}
//             />
//           </LineChart>
//         </ResponsiveContainer>
//       </div>

//       {/* GRID */}
//       <div
//         style={{
//           display: "grid",
//           gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
//           gap: "20px",
//         }}
//       >
//         {filteredData.map((item) => {
//           const color = getColor(item.level);

//           return (
//             <div
//               key={item.id}
//               style={{
//                 background: "#111827",
//                 padding: "18px",
//                 borderRadius: "12px",
//                 border: `1px solid ${color}`,
//                 minHeight: "220px",
//                 transition: "all 0.3s ease",
//                 boxShadow: `0 0 10px ${color}30`,
//                 cursor: "pointer",
//               }}
//               onMouseEnter={(e) => {
//                 e.currentTarget.style.transform = "translateY(-6px)";
//                 e.currentTarget.style.boxShadow = `0 0 18px ${color}`;
//               }}
//               onMouseLeave={(e) => {
//                 e.currentTarget.style.transform = "translateY(0)";
//                 e.currentTarget.style.boxShadow = `0 0 10px ${color}30`;
//               }}
//             >
//               <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
//                 <div style={{ minHeight: "100px" }}>
//                   <h3 style={{ fontSize: "16px" }}>{item.name}</h3>

//                   <p style={{ fontSize: "11px", color: "#6b7280" }}>
//                     Distributor ID: {item.id}
//                   </p>

//                   <h2 style={{ marginTop: "12px", fontSize: "38px" }}>
//                     {item.score}
//                   </h2>
//                 </div>

//                 <div style={{ marginTop: "auto" }}>
//                   <div
//                     style={{
//                       height: "6px",
//                       background: "#1f2937",
//                       borderRadius: "6px",
//                       overflow: "hidden",
//                       marginBottom: "10px",
//                     }}
//                   >
//                     <div
//                       style={{
//                         width: `${item.score}%`,
//                         height: "100%",
//                         background: color,
//                         transition: "width 1s ease",
//                       }}
//                     />
//                   </div>

//                   <span
//                     style={{
//                       fontSize: "11px",
//                       color: color,
//                       fontWeight: "600",
//                     }}
//                   >
//                     {item.level.toUpperCase()}
//                   </span>

//                   <div style={{ height: "16px", marginTop: "6px" }}>
//                     {item.level === "high" && (
//                       <span style={{ fontSize: "11px", color: "#dc2626" }}>
//                         Suspicious activity detected
//                       </span>
//                     )}
//                   </div>
//                 </div>
//               </div>
//             </div>
//           );
//         })}
//       </div>
//     </div>
//   );
// }

// export default RiskMonitor;

import React, { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

function RiskMonitor() {
  const [riskData, setRiskData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filter, setFilter] = useState("all");
  const [alert, setAlert] = useState("");

  const fetchData = async () => {
    try {
      const res = await fetch("http://127.0.0.1:8000/api/logs");
      const data = await res.json();

      // const logs = data.logs;
      const logs = data.logs
        .filter((log) => log.action === "honeypot_access")
        .slice(-10);   // 🔥 ONLY LAST 10 LOGS

      //  SORT logs by time
      logs.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

      let cumulativeScore = 0;

      const riskArray = logs.map((log) => {
        cumulativeScore += 30;

        return {
          id: log.timestamp,
          name: new Date(log.timestamp).toLocaleTimeString(),
          score: cumulativeScore,
          level:
            cumulativeScore >= 80
            ? "high"
            : cumulativeScore >= 40
            ? "medium"
            : "low",
        };
      });



      setRiskData(riskArray);
      setError("");

      if (riskArray.some((d) => d.level === "high")) {
        setAlert("⚠️ High Risk Distributor Detected!");
      } else {
        setAlert("");
      }

    } catch (err) {
      setError("Failed to load data");
    } finally {
      setLoading(false);
    }
  };

  

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const getColor = (level) => {
    if (level === "high") return "#dc2626";
    if (level === "medium") return "#ca8a04";
    return "#16a34a";
  };

  const filteredData =
    filter === "high"
      ? riskData.filter((item) => item.level === "high")
      : riskData;

  if (loading) {
    return (
      <div style={{ color: "white", paddingTop: "64px", padding: "20px" }}>
        <h2>Loading...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ color: "red", paddingTop: "64px", padding: "20px" }}>
        <h2>{error}</h2>
      </div>
    );
  }

  return (
    <div
      style={{
        paddingTop: "64px",   // 🔥 PERFECT ALIGN WITH NAVBAR
        paddingLeft: "20px",
        paddingRight: "20px",
        paddingBottom: "20px",
        background: "#050816",
        minHeight: "100vh",
        color: "white",
        fontFamily: "DM Sans, sans-serif",
      }}
    >
      {/* HEADER */}
      <h1 style={{ fontSize: "30px", marginBottom: "10px" }}>
        Risk Monitoring
      </h1>

      <p style={{ color: "#9ca3af", marginBottom: "20px" }}>
        Real-time distributor risk analysis and anomaly detection
      </p>

      {/* TIME */}
      <p style={{ fontSize: "12px", color: "#6b7280", marginBottom: "10px" }}>
        Last Updated: {new Date().toLocaleTimeString()}
      </p>

      {/* ALERT */}
      {alert && (
        <div
          style={{
            background: "#7f1d1d",
            padding: "12px",
            borderRadius: "8px",
            marginBottom: "15px",
            color: "#fecaca",
            fontWeight: "600",
            boxShadow: "0 0 10px rgba(220,38,38,0.4)",
          }}
        >
          {alert}
        </div>
      )}

      {/* HIGH RISK COUNT */}
      <p style={{ marginBottom: "20px", color: "#ef4444", fontWeight: "600" }}>
        High Risk Count: {riskData.filter((d) => d.level === "high").length}
      </p>

      {/* FILTER BUTTON */}
      <button
        onClick={() => setFilter(filter === "all" ? "high" : "all")}
        style={{
          marginBottom: "25px",
          padding: "10px 18px",
          borderRadius: "20px",
          border: "none",
          background: "#2563eb",
          color: "white",
          cursor: "pointer",
          fontWeight: "600",
        }}
      >
        {filter === "all" ? "Show High Risk Only" : "Show All"}
      </button>

      {/* CHART */}
      <div
        style={{
          background: "#111827",
          padding: "20px",
          borderRadius: "12px",
          marginBottom: "30px",
        }}
      >
        <h3 style={{ marginBottom: "15px" }}>Risk Overview</h3>

        <ResponsiveContainer width="100%" height={280}>
          <LineChart
            data={riskData}
            margin={{ top: 10, right: 10, left: 0, bottom: 10 }}
          >
            <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />

            <XAxis
              dataKey="name"
              interval={0}
              padding={{ left: 0, right: 0 }}
              tick={{ fill: "#9ca3af", fontSize: 11 }}
            />

            <YAxis
              domain={[0, 100]}
              tick={{ fill: "#9ca3af", fontSize: 11 }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                border: "1px solid #374151",
                color: "white",
              }}
            />

            <Line
              type="monotone"
              dataKey="score"
              stroke="#3b82f6"
              strokeWidth={3}
              dot={{ r: 5 }}
              activeDot={{ r: 7 }}
              animationDuration={1000}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* GRID */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
          gap: "20px",
        }}
      >
        {filteredData.map((item) => {
          const color = getColor(item.level);

          return (
            <div
              key={item.id}
              style={{
                background: "#111827",
                padding: "18px",
                borderRadius: "12px",
                border: `1px solid ${color}`,
                minHeight: "220px",
                transition: "all 0.3s ease",
                boxShadow: `0 0 10px ${color}30`,
                cursor: "pointer",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-6px)";
                e.currentTarget.style.boxShadow = `0 0 18px ${color}`;
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = `0 0 10px ${color}30`;
              }}
            >
              <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
                <div style={{ minHeight: "100px" }}>
                  <h3 style={{ fontSize: "16px" }}>{item.name}</h3>

                  <p style={{ fontSize: "11px", color: "#6b7280" }}>
                    Distributor ID: {item.id}
                  </p>

                  <h2 style={{ marginTop: "12px", fontSize: "38px" }}>
                    {item.score}
                  </h2>
                </div>

                <div style={{ marginTop: "auto" }}>
                  <div
                    style={{
                      height: "6px",
                      background: "#1f2937",
                      borderRadius: "6px",
                      overflow: "hidden",
                      marginBottom: "10px",
                    }}
                  >
                    <div
                      style={{
                        width: `${item.score}%`,
                        height: "100%",
                        background: color,
                        transition: "width 1s ease",
                      }}
                    />
                  </div>

                  <span
                    style={{
                      fontSize: "11px",
                      color: color,
                      fontWeight: "600",
                    }}
                  >
                    {item.level.toUpperCase()}
                  </span>

                  <div style={{ height: "16px", marginTop: "6px" }}>
                    {item.level === "high" && (
                      <span style={{ fontSize: "11px", color: "#dc2626" }}>
                        Suspicious activity detected
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default RiskMonitor;