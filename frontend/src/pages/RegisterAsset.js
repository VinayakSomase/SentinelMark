import React, { useState } from "react";

function RegisterAsset() {
  const [selectedDistributor, setSelectedDistributor] = useState("");
  const [video, setVideo] = useState(null);

  return (
    <div style={styles.container}>

      <div style={styles.card} className="card-hover">

        <h1 style={styles.logo}>🎬 Register Asset</h1>

        <p style={styles.desc}>
          Secure your content with forensic watermarking. Every frame becomes traceable and protected.
        </p>

        <select
          value={selectedDistributor}
          onChange={(e) => setSelectedDistributor(e.target.value)}
          style={styles.input}
        >
          <option value="">Select Distributor</option>
          <option>Star Sports</option>
          <option>Sony Liv</option>
          <option>JioCinema</option>
          <option>Zee Sports</option>
          <option>Other</option>
        </select>

        <input
          type="file"
          onChange={(e) => setVideo(e.target.files[0])}
          style={styles.file}
        />

        <button style={styles.button} className="btn-glow">
          🔐 Secure & Watermark
        </button>

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

  input: {
    width: "100%",
    padding: "12px",
    marginBottom: "15px",
    borderRadius: "10px",
    border: "none",
    outline: "none",
  },

  file: {
    width: "100%",
    marginBottom: "20px",
    color: "white",
  },

  button: {
    width: "100%",
    padding: "14px",
    background: "linear-gradient(90deg, #6366f1, #22c55e)",
    border: "none",
    borderRadius: "10px",
    color: "white",
    fontWeight: "bold",
    cursor: "pointer",
  },
};

export default RegisterAsset;