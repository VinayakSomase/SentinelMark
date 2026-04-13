import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={styles.navbar}>
      <div style={styles.logo}>🛡 SentinelMark</div>

      <div style={styles.navLinks}>
        <Link to="/" style={styles.link}>Home</Link>
        <Link to="/register" style={styles.link}>Register Asset</Link>
        <Link to="/detect" style={styles.link}>Detect Leak</Link>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    width: "100%",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "12px 40px",
    backgroundColor: "#0f172a",
    boxSizing: "border-box",   // 🔥 IMPORTANT FIX
  },

  logo: {
    color: "#38bdf8",
    fontSize: "20px",
    fontWeight: "bold",
  },

  navLinks: {
    display: "flex",
    gap: "20px",
    flexWrap: "wrap",   // 🔥 prevents overflow
  },

  link: {
    color: "white",
    textDecoration: "none",
    padding: "8px 16px",
    background: "#1e293b",
    borderRadius: "8px",
    transition: "0.3s",
  },
};

export default Navbar;