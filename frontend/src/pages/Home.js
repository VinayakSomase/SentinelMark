import React, { useEffect } from "react";
import { Link } from "react-router-dom";

function Home() {

  useEffect(() => {
    const elements = document.querySelectorAll(".fade");

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("show");
        }
      });
    });

    elements.forEach((el) => observer.observe(el));
  }, []);

  return (
    <div style={styles.container}>

      {/* SECTION 1 */}
      <section style={styles.hero} className="fade">
        <h1 style={styles.logo}>🛡 SentinelMark</h1>
        <p style={styles.tagline}>
          The future of anti-piracy intelligence
        </p>
      </section>

      {/* SECTION 2 */}
      <section style={styles.sectionLight} className="fade">
        <h2 style={styles.heading}>Predict Leaks Before They Happen</h2>
        <p style={styles.text}>
          AI monitors distributor behavior and flags suspicious activity before damage occurs.
        </p>
      </section>

      {/* SECTION 3 */}
      <section style={styles.sectionDark} className="fade">
        <h2 style={styles.heading}>Forensic Watermarking</h2>
        <p style={styles.text}>
          Every video is uniquely tagged. If leaked, we identify the exact source instantly.
        </p>
      </section>

      {/* SECTION 4 */}
      <section style={styles.sectionLight} className="fade">
        <h2 style={styles.heading}>Track Piracy Networks</h2>
        <p style={styles.text}>
          Our system maps how leaked content spreads across platforms in real-time.
        </p>
      </section>

      {/* SECTION 5 */}
      <section style={styles.finalSection} className="fade">

        {/* CARD 1 */}
        <div style={styles.card} className="card-hover">
          <h3>🎬 Register Asset</h3>
          <p>Secure your video with invisible identity tracking.</p>
          <Link to="/register" style={styles.buttonPrimary} className="btn-glow">
            Register Now →
          </Link>
        </div>

        {/* CARD 2 */}
        <div style={styles.card} className="card-hover">
          <h3>🕵️ Detect Leak</h3>
          <p>Upload leaked content and identify the source instantly.</p>
          <Link to="/detect" style={styles.buttonSecondary} className="btn-glow">
            Detect Source →
          </Link>
        </div>

      </section>

    </div>
  );
}

const styles = {
  container: {
    fontFamily: "Poppins, sans-serif",
  },

  hero: {
    height: "100vh",
    background: "linear-gradient(135deg, #020617, #0f172a)",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    color: "white",
    textAlign: "center",
  },

  logo: {
    fontSize: "60px",
    fontWeight: "bold",
    background: "linear-gradient(90deg, #38bdf8, #6366f1)",
    WebkitBackgroundClip: "text",
    color: "transparent",
  },

  tagline: {
    fontSize: "22px",
    color: "#cbd5f5",
  },

  sectionLight: {
    height: "100vh",
    background: "#f8fafc",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },

  sectionDark: {
    height: "100vh",
    background: "#020617",
    color: "white",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    textAlign: "center",
  },

  heading: {
    fontSize: "36px",
    marginBottom: "10px",
  },

  text: {
    fontSize: "18px",
    maxWidth: "600px",
  },

  finalSection: {
    height: "100vh",
    background: "#020617",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    gap: "40px",
  },

  card: {
    background: "#1e293b",
    padding: "30px",
    borderRadius: "15px",
    width: "300px",
    textAlign: "center",
    color: "white",
  },

  buttonPrimary: {
    display: "inline-block",
    marginTop: "15px",
    padding: "10px 20px",
    background: "#22c55e",
    color: "white",
    borderRadius: "8px",
    textDecoration: "none",
  },

  buttonSecondary: {
    display: "inline-block",
    marginTop: "15px",
    padding: "10px 20px",
    background: "#ef4444",
    color: "white",
    borderRadius: "8px",
    textDecoration: "none",
  },
};

export default Home;