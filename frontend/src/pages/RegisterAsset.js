import React, { useState, useEffect } from "react";

function RegisterAsset() {
  const [selectedDistributor, setSelectedDistributor] = useState("");
  const [video, setVideo] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [progress, setProgress] = useState(0);
  const [dragOver, setDragOver] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("in-view");
        });
      },
      { threshold: 0.1 }
    );
    document.querySelectorAll(".animate-section").forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  const handleSubmit = async () => {
  if (!selectedDistributor || !video) {
    alert("Please select a distributor and upload a video.");
    return;
  }

  setLoading(true);
  setProgress(10);

  try {
    const distributorMap = {
      "Star Sports": 2,
      "Sony Liv": 3,
      "JioCinema": 4,
      "Zee Sports": 5,
      "Other": 1
    };

    const distributor_id = distributorMap[selectedDistributor];

    const formData = new FormData();
    formData.append("distributor_id", distributor_id);
    formData.append("file", video);

    const res = await fetch("http://127.0.0.1:8000/api/register-asset", {
      method: "POST",
      body: formData
    });

    setProgress(50);

    const data = await res.json();
    console.log("Backend:", data);

    setProgress(80);

    if (data.success) {
      setProgress(100);
      setSuccess(true);
    } else {
      alert("Upload failed");
    }

  } catch (err) {
    console.error(err);
    alert("Backend connection error");
  }

  setLoading(false);
};

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("video/")) setVideo(file);
  };

  const loadingSteps = [
    { label: "Reading video frames", done: progress >= 35 },
    { label: "Generating forensic signature", done: progress >= 60 },
    { label: "Embedding watermark", done: progress >= 80 },
    { label: "Registering to distributor", done: progress >= 95 },
    { label: "Verifying integrity", done: progress >= 100 },
  ];

  return (
    <div style={styles.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
        * { box-sizing: border-box; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(28px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes checkIn {
          from { opacity: 0; transform: scale(0.5) rotate(-10deg); }
          to   { opacity: 1; transform: scale(1) rotate(0deg); }
        }
        @keyframes successGlow {
          0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0); }
          50%       { box-shadow: 0 0 30px rgba(34,197,94,0.15); }
        }
        @keyframes stepFade {
          from { opacity: 0; transform: translateX(-8px); }
          to   { opacity: 1; transform: translateX(0); }
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .hero-badge { animation: fadeUp 0.55s cubic-bezier(.22,.68,0,1.2) 0.05s both; }
        .hero-title { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.2s  both; }
        .hero-sub   { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.38s both; }
        .hero-stats { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.52s both; }

        .animate-section { opacity: 0; transform: translateY(32px); transition: opacity 0.7s ease, transform 0.7s ease; }
        .animate-section.in-view { opacity: 1; transform: translateY(0); }

        .select-field {
          width: 100%;
          padding: 11px 16px;
          background: #081510;
          border: 1.5px solid #22c55e;
          border-radius: 8px;
          color: white;
          font-size: 14px;
          outline: none;
          cursor: pointer;
          transition: border-color 0.2s ease, box-shadow 0.2s ease;
          font-family: 'DM Sans', sans-serif;
          appearance: none;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='%2322c55e' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
          background-repeat: no-repeat;
          background-position: right 14px center;
          padding-right: 40px;
        }
        .select-field:focus { border-color: #4ade80; box-shadow: 0 0 0 3px rgba(34,197,94,0.12); }
        .select-field option { background: #081510; }

        .upload-zone {
          display: block; width: 100%;
          padding: 2.25rem;
          background: #081510;
          border: 2px dashed #166534;
          border-radius: 10px;
          text-align: center;
          cursor: pointer;
          transition: border-color 0.25s ease, background 0.25s ease;
        }
        .upload-zone:hover, .upload-zone.drag-active {
          border-color: #22c55e;
          background: rgba(34,197,94,0.05);
        }

        .submit-btn {
          width: 100%; padding: 13px;
          background: #16a34a;
          border: 1px solid #22c55e;
          border-radius: 8px; color: white;
          font-size: 14px; font-weight: 500; cursor: pointer;
          margin-top: 0.5rem;
          font-family: 'DM Sans', sans-serif;
          transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }
        .submit-btn:hover:not(:disabled) {
          background: #15803d;
          transform: translateY(-1px);
          box-shadow: 0 6px 18px rgba(34,197,94,0.3);
        }
        .submit-btn:active:not(:disabled) { transform: translateY(0); }
        .submit-btn:disabled { background: #1f2937; color: #475569; cursor: not-allowed; border-color: #1f2937; }

        .reset-btn {
          padding: 12px 26px;
          background: rgba(34,197,94,0.1);
          border: 1px solid rgba(34,197,94,0.25);
          border-radius: 8px; color: #4ade80;
          font-size: 14px; cursor: pointer;
          font-family: 'DM Sans', sans-serif;
          transition: background 0.2s ease, transform 0.2s ease;
          font-weight: 500;
        }
        .reset-btn:hover { background: rgba(34,197,94,0.18); transform: translateY(-1px); }

        .success-card { animation: successGlow 2.5s ease-in-out infinite; }
        .check-icon { animation: checkIn 0.5s cubic-bezier(.22,.68,0,1.2) 0.1s both; }
        .loading-step { animation: stepFade 0.3s ease both; }
        .spinner {
          width: 16px; height: 16px;
          border: 2px solid rgba(34,197,94,0.2);
          border-top-color: #22c55e;
          border-radius: 50%;
          display: inline-block;
          animation: spin 0.7s linear infinite;
        }
      `}</style>

      {/* HERO */}
      <section style={styles.hero}>
        <div style={styles.heroBg}></div>
        <div style={{ position: "relative", zIndex: 1, textAlign: "center" }}>
          <div className="hero-badge" style={styles.badge}>🛡 Asset Registration</div>
          <h1 className="hero-title" style={styles.heroTitle}>Register Your Video Asset</h1>
          <p className="hero-sub" style={styles.heroSub}>
            Invisible forensic watermark, unique to each distributor. Leaks traced instantly.
          </p>
          <div className="hero-stats" style={styles.statsRow}>
            {[
              { num: "256-bit", label: "Encryption" },
              { num: "0%", label: "Quality Loss" },
              { num: "100%", label: "Traceable" },
            ].map((s, i) => (
              <React.Fragment key={i}>
                <div style={styles.stat}>
                  <div style={styles.statNum}>{s.num}</div>
                  <div style={styles.statLabel}>{s.label}</div>
                </div>
                {i < 2 && <div style={styles.statDivider}></div>}
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>

      {/* FORM SECTION */}
      <section style={styles.formSection}>

        {/* FORM CARD */}
        <div className="animate-section" style={styles.card}>
          {success ? (
            <div style={styles.successBox} className="success-card">
              <div style={styles.successIconWrap} className="check-icon">
                <span style={{ fontSize: "36px" }}>✅</span>
              </div>
              <h2 style={styles.successTitle}>Asset Registered!</h2>
              <p style={styles.successText}>
                Your video has been watermarked and registered to <strong style={{ color: "#e2e8f0" }}>{selectedDistributor}</strong>.
                Any leak will be traced back instantly.
              </p>
              <div style={styles.successMeta}>
                <div style={styles.successMetaRow}>
                  <span style={styles.metaLabel}>Distributor</span>
                  <span style={styles.metaVal}>{selectedDistributor}</span>
                </div>
                <div style={styles.successMetaRow}>
                  <span style={styles.metaLabel}>File</span>
                  <span style={styles.metaVal}>{video?.name}</span>
                </div>
                <div style={styles.successMetaRow}>
                  <span style={styles.metaLabel}>Status</span>
                  <span style={{ ...styles.metaVal, color: "#22c55e" }}>Protected ✓</span>
                </div>
              </div>
              <button className="reset-btn" onClick={() => { setSuccess(false); setVideo(null); setSelectedDistributor(""); setProgress(0); }}>
                Register Another →
              </button>
            </div>
          ) : (
            <>
              <h2 style={styles.cardTitle}>Upload & Watermark</h2>
              <p style={styles.cardSub}>Secure your content in seconds.</p>

              {/* STEP 1 — Distributor */}
              <div style={styles.fieldGroup}>
                <div style={styles.stepLabelRow}>
                  <span style={styles.stepBadge}>1</span>
                  <label style={styles.label}>Choose Distributor</label>
                </div>
                <p style={styles.stepHint}>Select who receives this watermarked copy — each gets a unique ID.</p>
                <select
                  className="select-field"
                  value={selectedDistributor}
                  onChange={(e) => setSelectedDistributor(e.target.value)}
                >
                  <option value="">Choose a distributor...</option>
                  {["Star Sports", "Sony Liv", "JioCinema", "Zee Sports", "Other"].map((d) => (
                    <option key={d}>{d}</option>
                  ))}
                </select>
              </div>

              {/* STEP 2 — Upload */}
              <div style={styles.fieldGroup}>
                <div style={styles.stepLabelRow}>
                  <span style={styles.stepBadge}>2</span>
                  <label style={styles.label}>Upload Video File</label>
                </div>
                <p style={styles.stepHint}>Drop your video below — watermark is embedded invisibly at pixel level.</p>
                <label
                  className={`upload-zone${dragOver ? " drag-active" : ""}`}
                  onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={handleDrop}
                >
                  <input type="file" accept="video/*" onChange={(e) => setVideo(e.target.files[0])} style={{ display: "none" }} />
                  {video ? (
                    <div>
                      <div style={{ fontSize: "26px", marginBottom: "0.5rem" }}>🎬</div>
                      <div style={styles.uploadText}>{video.name}</div>
                      <div style={styles.uploadHint}>Click or drag to change file</div>
                      <div style={{ marginTop: "8px", fontSize: "12px", color: "#4ade80", background: "rgba(34,197,94,0.1)", padding: "3px 10px", borderRadius: "100px", display: "inline-block" }}>
                        {(video.size / 1024 / 1024).toFixed(1)} MB
                      </div>
                    </div>
                  ) : (
                    <div>
                      <div style={styles.uploadIconWrap}>
                        <span style={{ fontSize: "22px" }}>📁</span>
                      </div>
                      <div style={styles.uploadText}>Click or drag video here</div>
                      <div style={styles.uploadHint}>MP4, AVI, MOV · Up to 10GB</div>
                      <div style={styles.uploadCta}>Browse files →</div>
                    </div>
                  )}
                </label>
              </div>

              <button className="submit-btn" onClick={handleSubmit} disabled={loading}>
                {loading ? (
                  <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                    <span className="spinner"></span>
                    Watermarking... {progress}%
                  </span>
                ) : "🔐 Secure & Watermark"}
              </button>

              {loading && (
                <div style={{ marginTop: "1.25rem" }}>
                  <div style={styles.progressTrack}>
                    <div style={{ ...styles.progressBar, width: `${progress}%`, transition: "width 0.4s ease" }}></div>
                  </div>
                  <div style={{ marginTop: "1rem", display: "flex", flexDirection: "column", gap: "8px" }}>
                    {loadingSteps.map((step, i) => (
                      <div key={i} className="loading-step" style={{ ...styles.loadingStep, animationDelay: `${i * 0.15}s` }}>
                        <span style={{ color: step.done ? "#22c55e" : "#334155", fontSize: "13px", transition: "color 0.3s ease" }}>
                          {step.done ? "✓" : "○"}
                        </span>
                        <span style={{ fontSize: "13px", color: step.done ? "#94a3b8" : "#475569", transition: "color 0.3s ease", textDecoration: step.done ? "line-through" : "none", fontFamily: "'DM Sans', sans-serif" }}>
                          {step.label}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </div>

        {/* INFO BOX */}
        <div className="animate-section" style={{ ...styles.infoBox, transitionDelay: "0.15s" }}>
          <h3 style={styles.infoTitle}>What happens next?</h3>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px", marginBottom: "1rem" }}>
            {[
              { num: "1", title: "Watermark embedded", text: "Unique ID embedded at pixel level, invisible to viewers." },
              { num: "2", title: "Asset registered", text: "Video logged to the selected distributor in our system." },
              { num: "3", title: "Protected forever", text: "Any leak is traced back to the exact source instantly." },
              { num: "4", title: "Report generated", text: "Full leak report with distributor details sent to you immediately." },
            ].map((s, i) => (
              <div key={i} style={styles.infoStepBox}>
                <div style={styles.infoNum}>{s.num}</div>
                <div style={styles.infoStepTitle}>{s.title}</div>
                <div style={styles.infoStepText}>{s.text}</div>
              </div>
            ))}
          </div>

          <div style={styles.securityBadge}>
            <span style={{ fontSize: "13px" }}>🔒</span>
            <span style={styles.securityText}>All uploads are encrypted in transit and at rest using AES-256.</span>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer style={styles.footer}>
        <span style={styles.footerLogo}>🛡 SentinelMark</span>
        <span style={styles.footerText}>The future of anti-piracy intelligence</span>
      </footer>
    </div>
  );
}

const styles = {
  page: { fontFamily: "'DM Sans', sans-serif", background: "#0a0f1a", color: "white", minHeight: "100vh", display: "flex", flexDirection: "column" },

  hero: { background: "#0a0f1a", padding: "5rem 2rem 3rem", textAlign: "center", position: "relative", overflow: "hidden" },
  heroBg: {
    position: "absolute", inset: 0, zIndex: 0,
    backgroundImage: "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)",
    backgroundSize: "50px 50px",
    maskImage: "radial-gradient(ellipse 80% 60% at 50% 50%, black, transparent)",
  },
  badge: { display: "inline-block", background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)", color: "#4ade80", fontSize: "12px", padding: "5px 16px", borderRadius: "100px", marginBottom: "1.25rem", fontWeight: "500", fontFamily: "'DM Sans', sans-serif" },
  heroTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "clamp(28px, 5vw, 42px)", fontWeight: "700", color: "#f1f5f9", marginBottom: "0.85rem", letterSpacing: "-0.02em" },
  heroSub: { fontFamily: "'DM Sans', sans-serif", color: "#64748b", fontSize: "14px", maxWidth: "400px", margin: "0 auto 2rem", lineHeight: "1.75" },
  statsRow: { display: "flex", gap: "2.5rem", justifyContent: "center", alignItems: "center", flexWrap: "wrap" },
  stat: { textAlign: "center" },
  statNum: { fontFamily: "'DM Sans', sans-serif", fontSize: "24px", fontWeight: "600", color: "#22c55e" },
  statLabel: { fontFamily: "'DM Sans', sans-serif", fontSize: "11px", color: "#475569", marginTop: "3px", letterSpacing: "0.05em", textTransform: "uppercase" },
  statDivider: { width: "1px", height: "32px", background: "#1f2937" },

  formSection: { display: "flex", gap: "2rem", padding: "3rem 2rem", maxWidth: "960px", margin: "0 auto", width: "100%", flex: 1, flexWrap: "wrap", justifyContent: "center", boxSizing: "border-box" },

  card: { background: "#0f172a", border: "1px solid #1a3a22", borderRadius: "14px", padding: "2rem", flex: "1 1 380px" },
  cardTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "20px", fontWeight: "600", color: "#f1f5f9", marginBottom: "0.25rem" },
  cardSub: { fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#64748b", marginBottom: "1.5rem" },

  fieldGroup: { marginBottom: "1.5rem", background: "rgba(34,197,94,0.03)", border: "1px solid rgba(34,197,94,0.1)", borderRadius: "10px", padding: "1rem" },

  stepLabelRow: { display: "flex", alignItems: "center", gap: "8px", marginBottom: "4px" },
  stepBadge: { width: "22px", height: "22px", borderRadius: "50%", background: "#166534", border: "1px solid #22c55e", color: "#4ade80", fontSize: "11px", fontWeight: "600", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontFamily: "'DM Sans', sans-serif" },
  label: { display: "block", fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#4ade80", fontWeight: "600", letterSpacing: "0.02em" },
  stepHint: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#475569", marginBottom: "10px", lineHeight: "1.5" },

  uploadIconWrap: { width: "48px", height: "48px", background: "#166534", borderRadius: "12px", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 12px" },
  uploadText: { fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#cbd5e1", marginBottom: "4px", fontWeight: "500" },
  uploadHint: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#475569" },
  uploadCta: { marginTop: "10px", fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#4ade80", fontWeight: "500" },

  progressTrack: { height: "4px", background: "#1f2937", borderRadius: "4px", overflow: "hidden" },
  progressBar: { height: "100%", background: "linear-gradient(90deg, #166534, #22c55e)", borderRadius: "4px" },
  loadingStep: { display: "flex", alignItems: "center", gap: "10px" },

  successBox: { textAlign: "center", padding: "0.5rem 0" },
  successIconWrap: { width: "72px", height: "72px", borderRadius: "50%", background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.2)", display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 1.25rem" },
  successTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "22px", fontWeight: "600", color: "#22c55e", marginBottom: "0.6rem" },
  successText: { fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#64748b", lineHeight: "1.7", marginBottom: "1.5rem" },
  successMeta: { background: "#111827", border: "1px solid #1a3a22", borderRadius: "10px", padding: "1rem", marginBottom: "1.5rem", textAlign: "left" },
  successMetaRow: { display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: "1px solid #1e293b", fontSize: "13px" },
  metaLabel: { fontFamily: "'DM Sans', sans-serif", color: "#475569" },
  metaVal: { fontFamily: "'DM Sans', sans-serif", color: "#cbd5e1", fontWeight: "500" },

  infoBox: { background: "#0f172a", border: "1px solid #1a3a22", borderRadius: "14px", padding: "2rem", flex: "1 1 280px", maxWidth: "340px", height: "fit-content" },
  infoTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "15px", fontWeight: "600", color: "#f1f5f9", marginBottom: "1.25rem" },

  infoStepBox: { background: "#111827", border: "1px solid #1a3a22", borderRadius: "10px", padding: "1rem" },
  infoNum: { width: "26px", height: "26px", borderRadius: "50%", background: "rgba(34,197,94,0.1)", border: "1px solid rgba(34,197,94,0.25)", color: "#22c55e", fontSize: "11px", fontWeight: "600", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: "0.6rem", fontFamily: "'DM Sans', sans-serif" },
  infoStepTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", fontWeight: "600", color: "#e2e8f0", marginBottom: "4px" },
  infoStepText: { fontFamily: "'DM Sans', sans-serif", fontSize: "11px", color: "#64748b", lineHeight: "1.6" },

  securityBadge: { display: "flex", alignItems: "flex-start", gap: "8px", background: "rgba(34,197,94,0.05)", border: "1px solid rgba(34,197,94,0.15)", borderRadius: "8px", padding: "10px 12px" },
  securityText: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#475569", lineHeight: "1.6" },

  footer: { background: "#060d1a", borderTop: "1px solid #1f2937", padding: "2rem", textAlign: "center", display: "flex", flexDirection: "column", gap: "6px", alignItems: "center" },
  footerLogo: { fontFamily: "'DM Sans', sans-serif", fontSize: "14px", fontWeight: "600", color: "#e2e8f0" },
  footerText: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#334155" },
};

export default RegisterAsset;


// import React, { useState, useEffect } from "react";

// function RegisterAsset() {
//   const [selectedDistributor, setSelectedDistributor] = useState("");
//   const [video, setVideo] = useState(null);
//   const [loading, setLoading] = useState(false);
//   const [success, setSuccess] = useState(false);
//   const [progress, setProgress] = useState(0);
//   const [dragOver, setDragOver] = useState(false);

//   useEffect(() => {
//     const observer = new IntersectionObserver(
//       (entries) => {
//         entries.forEach((entry) => {
//           if (entry.isIntersecting) entry.target.classList.add("in-view");
//         });
//       },
//       { threshold: 0.1 }
//     );
//     document.querySelectorAll(".animate-section").forEach((el) => observer.observe(el));
//     return () => observer.disconnect();
//   }, []);

//   // ✅ FIXED FUNCTION (REAL BACKEND CONNECTION)
//   const handleSubmit = async () => {
//     if (!selectedDistributor || !video) {
//       alert("Please select a distributor and upload a video.");
//       return;
//     }

//     setLoading(true);
//     setProgress(20);

//     try {
//       // map UI → backend IDs
//       const distributorMap = {
//         "Star Sports": 1,
//         "Sony Liv": 2,
//         "JioCinema": 3,
//         "Zee Sports": 4,
//         "Other": 5
//       };

//       const distributor_id = distributorMap[selectedDistributor];

//       const formData = new FormData();
//       formData.append("distributor_id", distributor_id);
//       formData.append("file", video);

//       const res = await fetch("http://127.0.0.1:8000/api/register-asset", {
//         method: "POST",
//         body: formData
//       });

//       const data = await res.json();
//       console.log("Backend response:", data);

//       if (data.success) {
//         setProgress(100);
//         setSuccess(true);
//       } else {
//         alert("Upload failed");
//       }

//     } catch (err) {
//       console.error(err);
//       alert("Backend not connected");
//     }

//     setLoading(false);
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     setDragOver(false);
//     const file = e.dataTransfer.files[0];
//     if (file && file.type.startsWith("video/")) setVideo(file);
//   };

//   return (
//     <div style={styles.page}>
      
//       <section style={styles.formSection}>

//         {/* FORM CARD */}
//         <div style={styles.card}>
//           {success ? (
//             <div style={styles.successBox}>
//               <h2 style={styles.successTitle}>✅ Asset Registered!</h2>
//               <p>
//                 Watermark applied successfully for <b>{selectedDistributor}</b>
//               </p>
//             </div>
//           ) : (
//             <>
//               <h2>Upload & Watermark</h2>

//               {/* DISTRIBUTOR */}
//               <select
//                 value={selectedDistributor}
//                 onChange={(e) => setSelectedDistributor(e.target.value)}
//               >
//                 <option value="">Choose distributor</option>
//                 <option>Star Sports</option>
//                 <option>Sony Liv</option>
//                 <option>JioCinema</option>
//                 <option>Zee Sports</option>
//                 <option>Other</option>
//               </select>

//               {/* FILE */}
//               <input
//                 type="file"
//                 accept="video/*"
//                 onChange={(e) => setVideo(e.target.files[0])}
//               />

//               <button onClick={handleSubmit} disabled={loading}>
//                 {loading ? "Uploading..." : "Secure & Watermark"}
//               </button>

//               <div>Progress: {progress}%</div>
//             </>
//           )}
//         </div>

//       </section>
//     </div>
//   );
// }

// const styles = {
//   page: { padding: "20px", color: "white", background: "#0a0f1a", minHeight: "100vh" },
//   formSection: { display: "flex", justifyContent: "center" },
//   card: { padding: "20px", background: "#111827", borderRadius: "10px" },
//   successBox: { textAlign: "center" },
//   successTitle: { color: "green" }
// };

// export default RegisterAsset;
