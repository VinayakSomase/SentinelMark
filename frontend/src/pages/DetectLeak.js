import React, { useState } from "react";

function DetectLeak() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState("");

  const handleDetect = () => {
    if (!video) {
      setResult("⚠️ Please upload a video first.");
      return;
    }

    // Demo result (you’ll connect backend later)
    setResult("🎯 Source: Sony Liv | Confidence: 97%");
  };

  return (
    <div style={styles.container}>

      <div style={styles.card} className="card-hover">

        <h1 style={styles.logo}>🕵️ Detect Leak</h1>

        <p style={styles.desc}>
          Upload suspicious content and instantly identify the source using forensic watermark detection.
        </p>

        <input
          type="file"
          onChange={(e) => setVideo(e.target.files[0])}
          style={styles.file}
        />

        <button style={styles.button} className="btn-glow" onClick={handleDetect}>
          🚨 Identify Source
        </button>

        {result && (
          <div style={styles.resultBox}>
            {result}
          </div>
        )}

      </div>

    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "linear-gradient(135deg, #020617, #0f172a)",
    fontFamily: "Poppins, sans-serif",
  },

  card: {
    background: "#1e293b",
    padding: "40px",
    borderRadius: "16px",
    width: "420px",
    textAlign: "center",
    color: "white",
  },

  logo: {
    fontSize: "32px",
    marginBottom: "10px",
  },

  desc: {
    color: "#cbd5f5",
    marginBottom: "25px",
    fontSize: "15px",
  },

  file: {
    width: "100%",
    marginBottom: "20px",
    color: "white",
  },

  button: {
    width: "100%",
    padding: "14px",
    background: "linear-gradient(90deg, #ef4444, #f97316)",
    border: "none",
    borderRadius: "10px",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },

  resultBox: {
    marginTop: "20px",
    padding: "15px",
    background: "#020617",
    borderRadius: "10px",
    fontSize: "16px",
  },
};

export default DetectLeak;