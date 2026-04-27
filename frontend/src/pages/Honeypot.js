
// import React, { useState, useEffect } from "react";

// function Honeypot() {
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [progress, setProgress] = useState(0);
//   const [drag, setDrag] = useState(false);

//   // fake progress animation
//   useEffect(() => {
//     let interval;
//     if (loading) {
//       interval = setInterval(() => {
//         setProgress((prev) => {
//           if (prev >= 100) return 100;
//           return prev + 10;
//         });
//       }, 150);
//     }
//     return () => clearInterval(interval);
//   }, [loading]);

//   const handleUpload = () => {
//     if (!file) return;

//     setLoading(true);
//     setProgress(0);
//     setResult(null);

//     setTimeout(() => {
//       setResult({
//         assetId: "ABC123",
//         distributor: "SonyLIV North",
//         status: "Trap Active",
//       });
//       setLoading(false);
//     }, 2000);
//   };

//   return (
//     <div style={styles.page}>
//       {/* HEADER */}
//       <div style={styles.header}>
//         <h1 style={styles.title}>Honeypot Protection</h1>
//         <p style={styles.subtitle}>
//           Create traceable traps using secure watermarking
//         </p>
//       </div>

//       {/* MAIN CARD */}
//       <div style={styles.card}>
//         {/* UPLOAD */}
//         <div
//           style={{
//             ...styles.uploadBox,
//             ...(drag ? styles.uploadActive : {}),
//           }}
//           onDragOver={(e) => {
//             e.preventDefault();
//             setDrag(true);
//           }}
//           onDragLeave={() => setDrag(false)}
//           onDrop={(e) => {
//             e.preventDefault();
//             setFile(e.dataTransfer.files[0]);
//             setDrag(false);
//           }}
//         >
//           <input
//             type="file"
//             onChange={(e) => setFile(e.target.files[0])}
//             style={styles.fileInput}
//           />

//           <p style={styles.fileText}>
//             {file ? file.name : "Drag & drop video or click to upload"}
//           </p>
//         </div>

//         {/* BUTTON */}
//         <button
//           style={{
//             ...styles.button,
//             ...(loading ? styles.buttonLoading : {}),
//           }}
//           onClick={handleUpload}
//           disabled={loading}
//         >
//           {loading ? "Processing..." : "Generate Honeypot"}
//         </button>

//         {/* PROGRESS BAR */}
//         {loading && (
//           <div style={styles.progressWrapper}>
//             <div style={styles.progressBar}>
//               <div
//                 style={{
//                   ...styles.progressFill,
//                   width: `${progress}%`,
//                 }}
//               />
//             </div>
//             <p style={styles.progressText}>{progress}% analyzing...</p>
//           </div>
//         )}

//         {/* AI SCAN TEXT */}
//         {loading && (
//           <div style={styles.scanText}>
//             🔍 Embedding watermark...
//           </div>
//         )}

//         {/* FEATURES */}
//         {!loading && (
//           <div style={styles.features}>
//             <p>✓ Secure watermark generated</p>
//             <p>✓ Unique distributor tracking</p>
//             <p>✓ Instant leak detection ready</p>
//           </div>
//         )}
//       </div>

//       {/* RESULT */}
//       {result && (
//         <div style={styles.resultCard}>
//           <h2>🎯 Honeypot Created Successfully</h2>

//           <div style={styles.resultItem}>
//             <span>Asset ID</span>
//             <strong>{result.assetId}</strong>
//           </div>

//           <div style={styles.resultItem}>
//             <span>Distributor</span>
//             <strong>{result.distributor}</strong>
//           </div>

//           <div style={styles.resultItem}>
//             <span>Status</span>
//             <strong style={{ color: "#22c55e" }}>{result.status}</strong>
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }

// const styles = {
//   page: {
//     padding: "100px 20px",
//     minHeight: "100vh",
//     background: "linear-gradient(135deg, #050816, #020617)",
//     color: "white",
//     textAlign: "center",
//   },

//   header: {
//     marginBottom: "40px",
//     animation: "fadeUp 0.6s ease",
//   },

//   title: {
//     fontSize: "36px",
//   },

//   subtitle: {
//     color: "#9ca3af",
//   },

//   card: {
//     maxWidth: "420px",
//     margin: "0 auto",
//     padding: "30px",
//     borderRadius: "16px",
//     background: "rgba(17, 24, 39, 0.7)",
//     backdropFilter: "blur(12px)",
//     border: "1px solid rgba(59,130,246,0.2)",
//     boxShadow: "0 0 30px rgba(59,130,246,0.25)",
//     animation: "fadeUp 0.8s ease",
//   },

//   uploadBox: {
//     border: "2px dashed #3b82f6",
//     borderRadius: "12px",
//     padding: "30px",
//     marginBottom: "20px",
//     cursor: "pointer",
//     transition: "0.3s",
//   },

//   uploadActive: {
//     background: "rgba(59,130,246,0.1)",
//     boxShadow: "0 0 20px rgba(59,130,246,0.6)",
//   },

//   fileInput: {
//     marginBottom: "10px",
//   },

//   fileText: {
//     fontSize: "13px",
//     color: "#9ca3af",
//   },

//   button: {
//     width: "100%",
//     padding: "12px",
//     borderRadius: "10px",
//     border: "none",
//     background: "linear-gradient(90deg, #2563eb, #3b82f6)",
//     color: "white",
//     fontWeight: "600",
//     cursor: "pointer",
//     boxShadow: "0 0 15px rgba(59,130,246,0.6)",
//   },

//   buttonLoading: {
//     opacity: 0.7,
//   },

//   progressWrapper: {
//     marginTop: "15px",
//   },

//   progressBar: {
//     height: "6px",
//     background: "#1f2937",
//     borderRadius: "6px",
//     overflow: "hidden",
//   },

//   progressFill: {
//     height: "100%",
//     background: "#3b82f6",
//     transition: "width 0.2s",
//   },

//   progressText: {
//     fontSize: "12px",
//     marginTop: "6px",
//     color: "#9ca3af",
//   },

//   scanText: {
//     marginTop: "10px",
//     fontSize: "13px",
//     color: "#60a5fa",
//     animation: "fadeIn 0.5s ease",
//   },

//   features: {
//     marginTop: "20px",
//     fontSize: "13px",
//     color: "#9ca3af",
//     textAlign: "left",
//   },

//   resultCard: {
//     marginTop: "40px",
//     padding: "25px",
//     borderRadius: "14px",
//     background: "#111827",
//     border: "1px solid #22c55e",
//     maxWidth: "420px",
//     marginInline: "auto",
//     boxShadow: "0 0 25px rgba(34,197,94,0.6)",
//     animation: "fadeUp 0.6s ease",
//   },

//   resultItem: {
//     display: "flex",
//     justifyContent: "space-between",
//     marginTop: "10px",
//     fontSize: "14px",
//   },
// };

// export default Honeypot;

// import React, { useState, useEffect } from "react";

// function Honeypot() {
//   const [file, setFile] = useState(null);
//   const [result, setResult] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [progress, setProgress] = useState(0);
//   const [drag, setDrag] = useState(false);

//   useEffect(() => {
//     let interval;
//     if (loading) {
//       interval = setInterval(() => {
//         setProgress((prev) => (prev >= 100 ? 100 : prev + 5));
//       }, 120);
//     }
//     return () => clearInterval(interval);
//   }, [loading]);

//   const [honeypotId, setHoneypotId] = useState(null);

//   const handleUpload = async () => {
//     if (!file) {
//       alert("Please upload a file");
//       return;
//     }

//     setLoading(true);
//     setProgress(0);
//     setResult(null);

//     const formData = new FormData();
//     formData.append("name", file.name);

//     try {
//       const res = await fetch("http://127.0.0.1:8000/api/create-honeypot", {
//         method: "POST",
//         body: formData,
//       });

//       const data = await res.json();

//       setHoneypotId(data.honeypot_id);

//       setResult({
//         assetId: data.honeypot_id,
//         distributor: "Decoy Trap",
//         status: "Trap Active",
//       });

//     } catch (err) {
//       alert("Error creating honeypot");
//     }

//     setLoading(false);
//   };

//   const handleAttack = async () => {
//     if (!honeypotId) {
//       alert("Create honeypot first");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("honeypot_id", honeypotId);
//     formData.append("ip", "192.168.1.10");

//     await fetch("http://127.0.0.1:8000/api/honeypot-access", {
//       method: "POST",
//       body: formData,
//     });

//     alert("🚨 Honeypot accessed!");
//   };
  

//   return (
//     <div style={styles.page}>
//       {/* BACKGROUND GLOW */}
//       <div style={styles.bgGlow}></div>

//       {/* HEADER */}
//       <div style={styles.header}>
//         <h1 style={styles.title}>Honeypot Protection</h1>
//         <p style={styles.subtitle}>
//           Create traceable traps using secure watermarking
//         </p>
//       </div>

//       {/* CARD */}
//       <div style={styles.card}>
//         {/* UPLOAD */}
//         <div
//           style={{
//             ...styles.uploadBox,
//             ...(drag ? styles.uploadActive : {}),
//           }}
//           onDragOver={(e) => {
//             e.preventDefault();
//             setDrag(true);
//           }}
//           onDragLeave={() => setDrag(false)}
//           onDrop={(e) => {
//             e.preventDefault();
//             setFile(e.dataTransfer.files[0]);
//             setDrag(false);
//           }}
//         >
//           <input
//             type="file"
//             onChange={(e) => setFile(e.target.files[0])}
//             style={styles.fileInput}
//           />

//           <p style={styles.fileText}>
//             {file ? file.name : "Drag & drop video or click to upload"}
//           </p>
//         </div>

//         {/* BUTTON */}
//         <button
//           style={{
//             ...styles.button,
//             ...(loading ? styles.buttonLoading : {}),
//           }}
//           onClick={handleUpload}
//           disabled={loading}
//         >
//           {loading ? "Processing..." : "Generate Honeypot"}
//         </button>

//         {/* PROGRESS */}
//         {loading && (
//           <>
//             <div style={styles.progressWrapper}>
//               <div style={styles.progressBar}>
//                 <div
//                   style={{
//                     ...styles.progressFill,
//                     width: `${progress}%`,
//                   }}
//                 />
//               </div>
//               <p style={styles.progressText}>{progress}% analyzing...</p>
//             </div>

//             <div style={styles.scanText}>
//               🔍 Embedding invisible watermark...
//             </div>
//           </>
//         )}

//         {/* FEATURES */}
//         {!loading && (
//           <div style={styles.features}>
//             <p>✓ Secure watermark generated</p>
//             <p>✓ Unique distributor tracking</p>
//             <p>✓ Instant leak detection ready</p>
//           </div>
//         )}
//       </div>

//       {result && (
//         <div style={styles.resultCard}>
//           <h2>🎯 Honeypot Created</h2>

//           <div style={styles.resultItem}>
//             <span>Asset ID</span>
//             <strong>{result.assetId}</strong>
//           </div>

//           <div style={styles.resultItem}>
//             <span>Distributor</span>
//             <strong>{result.distributor}</strong>
//           </div>

//           <div style={styles.resultItem}>
//             <span>Status</span>
//             <strong style={{ color: "#22c55e" }}>{result.status}</strong>
//           </div>

//           <button
//             style={{
//               ...styles.button,
//               marginTop: "15px",
//               background: "linear-gradient(90deg, #ef4444, #dc2626)",
//             }}
//             onClick={handleAttack}
//           >
//             🚨 Simulate Attack
//           </button>
//         </div>
//       )}
      

// const styles = {
//   page: {
//     padding: "100px 20px",
//     minHeight: "100vh",
//     background: "radial-gradient(circle at 20% 20%, #0a1a3a, #020617)",
//     color: "white",
//     textAlign: "center",
//     position: "relative",
//     overflow: "hidden",
//   },

//   bgGlow: {
//     position: "absolute",
//     width: "500px",
//     height: "500px",
//     background: "radial-gradient(circle, rgba(59,130,246,0.3), transparent)",
//     top: "-100px",
//     left: "-100px",
//     filter: "blur(100px)",
//     animation: "float 6s ease-in-out infinite",
//   },

//   header: {
//     marginBottom: "40px",
//     animation: "fadeUp 0.6s ease",
//   },

//   title: {
//     fontSize: "38px",
//     fontWeight: "700",
//   },

//   subtitle: {
//     color: "#9ca3af",
//   },

//   card: {
//     maxWidth: "420px",
//     margin: "0 auto",
//     padding: "30px",
//     borderRadius: "16px",
//     background: "rgba(17, 24, 39, 0.7)",
//     backdropFilter: "blur(14px)",
//     border: "1px solid rgba(59,130,246,0.3)",
//     boxShadow: "0 0 40px rgba(59,130,246,0.25)",
//     animation: "fadeUp 0.8s ease",
//   },

//   uploadBox: {
//     border: "2px dashed #3b82f6",
//     borderRadius: "12px",
//     padding: "30px",
//     marginBottom: "20px",
//     cursor: "pointer",
//     transition: "0.3s",
//   },

//   uploadActive: {
//     background: "rgba(59,130,246,0.1)",
//     boxShadow: "0 0 25px rgba(59,130,246,0.7)",
//     transform: "scale(1.02)",
//   },

//   fileInput: {
//     marginBottom: "10px",
//   },

//   fileText: {
//     fontSize: "13px",
//     color: "#9ca3af",
//   },

//   button: {
//     width: "100%",
//     padding: "12px",
//     borderRadius: "10px",
//     border: "none",
//     background: "linear-gradient(90deg, #2563eb, #3b82f6)",
//     color: "white",
//     fontWeight: "600",
//     cursor: "pointer",
//     boxShadow: "0 0 20px rgba(59,130,246,0.7)",
//     transition: "0.3s",
//   },

//   buttonLoading: {
//     opacity: 0.7,
//   },

//   progressWrapper: {
//     marginTop: "15px",
//   },

//   progressBar: {
//     height: "6px",
//     background: "#1f2937",
//     borderRadius: "6px",
//     overflow: "hidden",
//   },

//   progressFill: {
//     height: "100%",
//     background: "linear-gradient(90deg, #22c55e, #3b82f6)",
//     transition: "width 0.2s",
//   },

//   progressText: {
//     fontSize: "12px",
//     marginTop: "6px",
//     color: "#9ca3af",
//   },

//   scanText: {
//     marginTop: "10px",
//     fontSize: "13px",
//     color: "#60a5fa",
//     animation: "fadeIn 0.5s ease",
//   },

//   features: {
//     marginTop: "20px",
//     fontSize: "13px",
//     color: "#9ca3af",
//     textAlign: "left",
//   },

//   resultCard: {
//     marginTop: "40px",
//     padding: "25px",
//     borderRadius: "14px",
//     background: "#111827",
//     border: "1px solid #22c55e",
//     maxWidth: "420px",
//     marginInline: "auto",
//     boxShadow: "0 0 30px rgba(34,197,94,0.7)",
//     animation: "fadeUp 0.6s ease",
//   },

//   resultItem: {
//     display: "flex",
//     justifyContent: "space-between",
//     marginTop: "12px",
//     fontSize: "14px",
//   },
// };

// export default Honeypot;




import React, { useState, useEffect } from "react";

function Honeypot() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [drag, setDrag] = useState(false);
  const [honeypotId, setHoneypotId] = useState(null);

  useEffect(() => {
    let interval;
    if (loading) {
      interval = setInterval(() => {
        setProgress((prev) => (prev >= 100 ? 100 : prev + 5));
      }, 120);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a file");
      return;
    }

    setLoading(true);
    setProgress(0);
    setResult(null);

    const formData = new FormData();
    formData.append("name", file.name);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/create-honeypot", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      setHoneypotId(data.honeypot_id);

      setResult({
        assetId: data.honeypot_id,
        distributor: "Decoy Trap",
        status: "Trap Active",
      });
    } catch (err) {
      alert("Error creating honeypot");
    }

    setLoading(false);
  };

  const handleAttack = async () => {
    if (!honeypotId) {
      alert("Create honeypot first");
      return;
    }

    const formData = new FormData();
    formData.append("honeypot_id", honeypotId);
    formData.append("ip", "192.168.1.10");

    await fetch("http://127.0.0.1:8000/api/honeypot-access", {
      method: "POST",
      body: formData,
    });

    alert("🚨 Honeypot accessed!");
  };

  return (
    <div style={styles.page}>
      <div style={styles.bgGlow}></div>

      <div style={styles.header}>
        <h1 style={styles.title}>Honeypot Protection</h1>
        <p style={styles.subtitle}>
          Create traceable traps using secure watermarking
        </p>
      </div>

      <div style={styles.card}>
        <div
          style={{
            ...styles.uploadBox,
            ...(drag ? styles.uploadActive : {}),
          }}
          onDragOver={(e) => {
            e.preventDefault();
            setDrag(true);
          }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => {
            e.preventDefault();
            setFile(e.dataTransfer.files[0]);
            setDrag(false);
          }}
        >
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
            style={styles.fileInput}
          />

          <p style={styles.fileText}>
            {file ? file.name : "Drag & drop video or click to upload"}
          </p>
        </div>

        <button
          style={{
            ...styles.button,
            ...(loading ? styles.buttonLoading : {}),
          }}
          onClick={handleUpload}
          disabled={loading}
        >
          {loading ? "Processing..." : "Generate Honeypot"}
        </button>

        {loading && (
          <>
            <div style={styles.progressWrapper}>
              <div style={styles.progressBar}>
                <div
                  style={{
                    ...styles.progressFill,
                    width: `${progress}%`,
                  }}
                />
              </div>
              <p style={styles.progressText}>{progress}% analyzing...</p>
            </div>

            <div style={styles.scanText}>
              🔍 Embedding invisible watermark...
            </div>
          </>
        )}

        {!loading && (
          <div style={styles.features}>
            <p>✓ Secure watermark generated</p>
            <p>✓ Unique distributor tracking</p>
            <p>✓ Instant leak detection ready</p>
          </div>
        )}
      </div>

      {result && (
        <div style={styles.resultCard}>
          <h2>🎯 Honeypot Created</h2>

          <div style={styles.resultItem}>
            <span>Asset ID</span>
            <strong>{result.assetId}</strong>
          </div>

          <div style={styles.resultItem}>
            <span>Distributor</span>
            <strong>{result.distributor}</strong>
          </div>

          <div style={styles.resultItem}>
            <span>Status</span>
            <strong style={{ color: "#22c55e" }}>{result.status}</strong>
          </div>

          <button
            style={{
              ...styles.button,
              marginTop: "15px",
              background: "linear-gradient(90deg, #ef4444, #dc2626)",
            }}
            onClick={handleAttack}
          >
            🚨 Simulate Attack
          </button>
        </div>
      )}
    </div>
  );
}

const styles = {
  page: {
    padding: "100px 20px",
    minHeight: "100vh",
    background: "radial-gradient(circle at 20% 20%, #0a1a3a, #020617)",
    color: "white",
    textAlign: "center",
    position: "relative",
    overflow: "hidden",
  },

  bgGlow: {
    position: "absolute",
    width: "500px",
    height: "500px",
    background: "radial-gradient(circle, rgba(59,130,246,0.3), transparent)",
    top: "-100px",
    left: "-100px",
    filter: "blur(100px)",
  },

  header: {
    marginBottom: "40px",
  },

  title: {
    fontSize: "38px",
    fontWeight: "700",
  },

  subtitle: {
    color: "#9ca3af",
  },

  card: {
    maxWidth: "420px",
    margin: "0 auto",
    padding: "30px",
    borderRadius: "16px",
    background: "rgba(17, 24, 39, 0.7)",
    backdropFilter: "blur(14px)",
    border: "1px solid rgba(59,130,246,0.3)",
    boxShadow: "0 0 40px rgba(59,130,246,0.25)",
  },

  uploadBox: {
    border: "2px dashed #3b82f6",
    borderRadius: "12px",
    padding: "30px",
    marginBottom: "20px",
    cursor: "pointer",
  },

  uploadActive: {
    background: "rgba(59,130,246,0.1)",
  },

  fileInput: {
    marginBottom: "10px",
  },

  fileText: {
    fontSize: "13px",
    color: "#9ca3af",
  },

  button: {
    width: "100%",
    padding: "12px",
    borderRadius: "10px",
    border: "none",
    background: "linear-gradient(90deg, #2563eb, #3b82f6)",
    color: "white",
    fontWeight: "600",
    cursor: "pointer",
  },

  buttonLoading: {
    opacity: 0.7,
  },

  progressWrapper: {
    marginTop: "15px",
  },

  progressBar: {
    height: "6px",
    background: "#1f2937",
    borderRadius: "6px",
    overflow: "hidden",
  },

  progressFill: {
    height: "100%",
    background: "linear-gradient(90deg, #22c55e, #3b82f6)",
  },

  progressText: {
    fontSize: "12px",
    marginTop: "6px",
    color: "#9ca3af",
  },

  scanText: {
    marginTop: "10px",
    fontSize: "13px",
    color: "#60a5fa",
  },

  features: {
    marginTop: "20px",
    fontSize: "13px",
    color: "#9ca3af",
    textAlign: "left",
  },

  resultCard: {
    marginTop: "40px",
    padding: "25px",
    borderRadius: "14px",
    background: "#111827",
    border: "1px solid #22c55e",
    maxWidth: "420px",
    marginInline: "auto",
  },

  resultItem: {
    display: "flex",
    justifyContent: "space-between",
    marginTop: "12px",
    fontSize: "14px",
  },
};

export default Honeypot;