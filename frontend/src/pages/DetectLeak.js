import React, { useState, useEffect } from "react";

function DetectLeak() {
  const [video, setVideo] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [currentPhase, setCurrentPhase] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const [confidenceAnim, setConfidenceAnim] = useState(0);

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

  useEffect(() => {
    if (result) {
      let start = 0;
      const target = result.confidence;
      const duration = 1200;
      const startTime = performance.now();
      const tick = (now) => {
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        start = Math.round(eased * target);
        setConfidenceAnim(start);
        if (progress < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    }
  }, [result]);

  const handleDetect = async () => {
  if (!video) {
    alert("Please upload a video first.");
    return;
  }

  setLoading(true);
  setResult(null);
  setProgress(10);
  setCurrentPhase("Uploading video...");

  try {
    const formData = new FormData();
    formData.append("file", video);

    const res = await fetch("http://127.0.0.1:8000/api/detect-leak", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    const phases = [
      { phase: "Extracting video frames...", p: 30, t: 400 },
      { phase: "Scanning watermark...", p: 60, t: 600 },
      { phase: "Matching distributor...", p: 85, t: 500 },
    ];

    let delay = 0;
    phases.forEach(({ phase, p, t }) => {
      delay += t;
      setTimeout(() => {
        setCurrentPhase(phase);
        setProgress(p);
      }, delay);
    });

    setTimeout(() => {
      setLoading(false);
      setProgress(100);

      if (data.leak_detected) {
        setResult({
          source: data.distributor_name,
          confidence: Math.round(data.confidence),
          distributorId: data.distributor_id || "N/A",
          detectedAt: data.detected_at,
          region: "India",
          riskLevel: data.confidence > 75 ? "HIGH" : "LOW",
          report: data.evidence_report,
        });
      } else {
        alert(data.message || "No watermark found");
      }
    }, delay + 500);

  } catch (err) {
    console.error(err);
    setLoading(false);
    alert("Backend not connected ❌");
  }
};

  return (
    <div style={styles.page}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
        * { box-sizing: border-box; }
        @keyframes fadeUp { from { opacity: 0; transform: translateY(28px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes resultSlideIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes riskBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0.6; } }
        @keyframes confidenceBar { from { width: 0%; } }
        @keyframes uploadPulse {
          0%, 100% { border-color: rgba(239,68,68,0.5); box-shadow: 0 0 0 0 rgba(239,68,68,0); }
          50% { border-color: rgba(239,68,68,0.85); box-shadow: 0 0 0 6px rgba(239,68,68,0.08); }
        }
        .hero-badge { animation: fadeUp 0.55s cubic-bezier(.22,.68,0,1.2) 0.05s both; }
        .hero-title { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.2s both; }
        .hero-sub   { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.38s both; }
        .animate-section { opacity: 0; transform: translateY(32px); transition: opacity 0.7s ease, transform 0.7s ease; }
        .animate-section.in-view { opacity: 1; transform: translateY(0); }
        .upload-zone {
          display: block; width: 100%; padding: 2.75rem 2rem;
          background: rgba(220,38,38,0.06); border: 2px dashed rgba(239,68,68,0.5);
          border-radius: 12px; text-align: center; cursor: pointer;
          transition: border-color 0.25s ease, background 0.25s ease, box-shadow 0.25s ease;
          margin-bottom: 1.25rem; animation: uploadPulse 2.5s ease-in-out infinite;
        }
        .upload-zone:hover, .upload-zone.drag-active { border-color: #ef4444; background: rgba(239,68,68,0.11); animation: none; box-shadow: 0 0 0 4px rgba(239,68,68,0.1); }
        .upload-zone.has-file { animation: none; border-color: rgba(239,68,68,0.6); background: rgba(239,68,68,0.08); }
        .detect-btn {
          width: 100%; padding: 14px; background: #dc2626; border: 1px solid #ef4444;
          border-radius: 8px; color: white; font-size: 15px; font-weight: 600; cursor: pointer;
          font-family: 'DM Sans', sans-serif;
          transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; letter-spacing: 0.02em;
        }
        .detect-btn:hover:not(:disabled) { background: #ef4444; transform: translateY(-1px); box-shadow: 0 6px 18px rgba(220,38,38,0.3); }
        .detect-btn:active:not(:disabled) { transform: translateY(0); }
        .detect-btn:disabled { background: #1f2937; color: #475569; cursor: not-allowed; border-color: #1f2937; }
        .result-box { animation: resultSlideIn 0.5s cubic-bezier(.22,.68,0,1.2) both; }
        .spinner { width: 16px; height: 16px; border: 2px solid rgba(239,68,68,0.2); border-top-color: #ef4444; border-radius: 50%; display: inline-block; animation: spin 0.7s linear infinite; }
        .risk-high { animation: riskBlink 1.5s ease-in-out infinite; }
        .confidence-bar { animation: confidenceBar 1.2s cubic-bezier(.22,.68,0,1.2) 0.3s both; }
        .report-btn {
          width: 100%; margin-top: 1rem; padding: 10px;
          background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2);
          border-radius: 8px; color: #f87171; font-size: 14px; cursor: pointer;
          font-family: 'DM Sans', sans-serif; font-weight: 500;
          transition: background 0.2s ease, transform 0.2s ease;
        }
        .report-btn:hover { background: rgba(239,68,68,0.14); transform: translateY(-1px); }
      `}</style>

      <section style={styles.hero}>
        <div style={styles.heroBg}></div>
        <div style={{ position: "relative", zIndex: 1, textAlign: "center" }}>
          <div className="hero-badge" style={styles.badge}>🕵️ Leak Detection</div>
          <h1 className="hero-title" style={styles.heroTitle}>Detect Video Leak Source</h1>
          <p className="hero-sub" style={styles.heroSub}>
            Upload any suspicious video — our AI identifies the exact source distributor instantly.
          </p>
        </div>
      </section>

      <section style={styles.mainSection}>
        <div className="animate-section" style={styles.card}>
          <h2 style={styles.cardTitle}>Upload Suspicious Video</h2>
          <p style={styles.cardSub}>We'll analyze it and identify where the leak came from.</p>

          <label
            className={`upload-zone${dragOver ? " drag-active" : ""}${video ? " has-file" : ""}`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault(); setDragOver(false);
              const f = e.dataTransfer.files[0];
              if (f?.type.startsWith("video/")) { setVideo(f); setResult(null); }
            }}
          >
            <input type="file" accept="video/*" onChange={(e) => { setVideo(e.target.files[0]); setResult(null); }} style={{ display: "none" }} />
            {video ? (
              <div>
                <div style={{ fontSize: "32px", marginBottom: "0.5rem" }}>🎬</div>
                <div style={styles.uploadTextActive}>{video.name}</div>
                <div style={styles.uploadHint}>Click or drag to change file</div>
                <div style={styles.fileSizeBadge}>{(video.size / 1024 / 1024).toFixed(1)} MB</div>
              </div>
            ) : (
              <div>
                <div style={{ fontSize: "38px", marginBottom: "1rem" }}>📁</div>
                <div style={styles.uploadTextMain}>Click or drag video here</div>
                <div style={styles.uploadTextSub}>MP4, AVI, MOV supported</div>
                <div style={styles.uploadCta}>← tap to browse files</div>
              </div>
            )}
          </label>

          <button className="detect-btn" onClick={handleDetect} disabled={loading}>
            {loading ? (
              <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                <span className="spinner"></span>
                {currentPhase || "Analyzing..."}
              </span>
            ) : "🚨 Identify Leak Source"}
          </button>

          {loading && (
            <div style={{ marginTop: "1rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                <span style={{ fontSize: "12px", color: "#475569", fontFamily: "'DM Sans', sans-serif" }}>Analysis progress</span>
                <span style={{ fontSize: "12px", color: "#ef4444", fontWeight: "600", fontFamily: "'DM Sans', sans-serif" }}>{progress}%</span>
              </div>
              <div style={styles.progressTrack}>
                <div style={{ ...styles.progressBar, width: `${progress}%`, transition: "width 0.45s ease" }}></div>
              </div>
            </div>
          )}

          {result && (
            <div style={styles.resultBox} className="result-box">
              <div style={styles.resultHeader}>
                <span style={styles.resultBadge}>🎯 Leak Confirmed</span>
                <span style={styles.riskBadge} className="risk-high">{result.riskLevel} RISK</span>
              </div>
              <div style={styles.confidenceMeter}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "6px" }}>
                  <span style={{ fontSize: "12px", color: "#475569", fontFamily: "'DM Sans', sans-serif" }}>Confidence Score</span>
                  <span style={{ fontSize: "14px", fontWeight: "700", color: "#22c55e", fontFamily: "'DM Sans', sans-serif" }}>{confidenceAnim}%</span>
                </div>
                <div style={{ height: "6px", background: "#1e293b", borderRadius: "6px", overflow: "hidden" }}>
                  <div className="confidence-bar" style={{ height: "100%", width: `${result.confidence}%`, background: "linear-gradient(90deg, #16a34a, #22c55e)", borderRadius: "6px" }}></div>
                </div>
              </div>
              {[
                { label: "Source Distributor", val: result.source, color: "#e2e8f0" },
                { label: "Distributor ID", val: result.distributorId, color: "#e2e8f0" },
                { label: "Region", val: result.region, color: "#e2e8f0" },
                { label: "Detected At", val: result.detectedAt, color: "#94a3b8" },
              ].map((row, i) => (
                <div key={i} style={styles.resultRow}>
                  <span style={styles.resultLabel}>{row.label}</span>
                  <span style={{ ...styles.resultVal, color: row.color }}>{row.val}</span>
                </div>
              ))}
              <button
                className="report-btn"
                onClick={() => {
                  const url = `http://127.0.0.1:8000/${result.report}`;
                  console.log("Opening:", url);
                  window.open(url, "_blank");
                }}
              >
                📄 Download Full Report
              </button>
            </div>
          )}
        </div>

        <div style={styles.infoCol}>
          <div className="animate-section" style={{ ...styles.infoBox, transitionDelay: "0.15s" }}>
            <h3 style={styles.infoTitle}>How detection works</h3>
            <div style={styles.infoSteps}>
              {[
                { num: "1", title: "Video analyzed", text: "Our AI scans every frame for the invisible watermark signature embedded at the pixel level." },
                { num: "2", title: "Watermark extracted", text: "The unique distributor ID is decrypted from the forensic payload embedded in the video." },
                { num: "3", title: "Source identified", text: "We match the ID against our distributor database and reveal the exact leak origin." },
              ].map((s, i) => (
                <div key={i} style={styles.infoStep}>
                  <div style={styles.infoNum}>{s.num}</div>
                  <div>
                    <div style={styles.infoStepTitle}>{s.title}</div>
                    <div style={styles.infoStepText}>{s.text}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="animate-section" style={{ ...styles.warningBox, transitionDelay: "0.3s" }}>
            <div style={{ fontSize: "16px", flexShrink: 0 }}>⚠️</div>
            <div style={styles.warningText}>Only upload content you are authorized to investigate. All detection requests are logged and audited for legal compliance.</div>
          </div>
        </div>
      </section>

      <footer style={styles.footer}>
        <span style={styles.footerLogo}>🛡 SentinelMark</span>
        <span style={styles.footerText}>The future of anti-piracy intelligence</span>
      </footer>
    </div>
  );
}

const styles = {
  page: { fontFamily: "'DM Sans', sans-serif", background: "#0a0f1a", color: "white", minHeight: "100vh", display: "flex", flexDirection: "column" },
  hero: { background: "#0a0f1a", padding: "5rem 2rem 3.5rem", textAlign: "center", position: "relative", overflow: "hidden" },
  heroBg: { position: "absolute", inset: 0, zIndex: 0, backgroundImage: "linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px)", backgroundSize: "50px 50px", maskImage: "radial-gradient(ellipse 80% 60% at 50% 50%, black, transparent)" },
  badge: { display: "inline-block", background: "rgba(220,38,38,0.1)", border: "1px solid rgba(239,68,68,0.25)", color: "#fca5a5", fontSize: "13px", padding: "6px 18px", borderRadius: "100px", marginBottom: "1.5rem", fontWeight: "500", fontFamily: "'DM Sans', sans-serif" },
  heroTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "clamp(32px, 5vw, 48px)", fontWeight: "700", color: "#f1f5f9", marginBottom: "1rem", letterSpacing: "-0.02em" },
  heroSub: { fontFamily: "'DM Sans', sans-serif", color: "#64748b", fontSize: "15px", maxWidth: "460px", margin: "0 auto", lineHeight: "1.8", fontWeight: "300" },
  mainSection: { display: "flex", gap: "2rem", padding: "3rem 2rem", maxWidth: "960px", margin: "0 auto", width: "100%", flex: 1, flexWrap: "wrap", justifyContent: "center", boxSizing: "border-box" },
  card: { background: "#0f172a", border: "1px solid #1f2937", borderRadius: "14px", padding: "2.25rem", flex: "1 1 380px" },
  cardTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "22px", fontWeight: "700", color: "#f1f5f9", marginBottom: "0.3rem" },
  cardSub: { fontFamily: "'DM Sans', sans-serif", fontSize: "14px", color: "#64748b", marginBottom: "1.75rem", fontWeight: "300" },
  uploadTextMain: { fontFamily: "'DM Sans', sans-serif", fontSize: "16px", color: "#f87171", fontWeight: "600", marginBottom: "6px" },
  uploadTextSub: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#475569", marginBottom: "10px" },
  uploadCta: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "rgba(239,68,68,0.5)", marginTop: "8px", letterSpacing: "0.03em" },
  uploadTextActive: { fontFamily: "'DM Sans', sans-serif", fontSize: "14px", color: "#cbd5e1", marginBottom: "4px", fontWeight: "500" },
  uploadHint: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#475569" },
  fileSizeBadge: { marginTop: "8px", fontSize: "12px", color: "#dc2626", background: "rgba(239,68,68,0.1)", padding: "3px 10px", borderRadius: "100px", display: "inline-block", fontFamily: "'DM Sans', sans-serif" },
  progressTrack: { height: "4px", background: "#1f2937", borderRadius: "4px", overflow: "hidden" },
  progressBar: { height: "100%", background: "linear-gradient(90deg, #991b1b, #ef4444)", borderRadius: "4px" },
  resultBox: { marginTop: "1.5rem", background: "#111827", border: "1px solid rgba(239,68,68,0.2)", borderRadius: "12px", padding: "1.5rem" },
  resultHeader: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1.25rem" },
  resultBadge: { background: "rgba(239,68,68,0.1)", border: "1px solid rgba(239,68,68,0.25)", color: "#f87171", fontSize: "13px", padding: "4px 12px", borderRadius: "100px", fontWeight: "600", fontFamily: "'DM Sans', sans-serif" },
  riskBadge: { background: "rgba(239,68,68,0.15)", color: "#ef4444", fontSize: "11px", padding: "3px 8px", borderRadius: "100px", fontWeight: "700", letterSpacing: "0.05em", fontFamily: "'DM Sans', sans-serif" },
  confidenceMeter: { background: "#0f172a", border: "1px solid #1f2937", borderRadius: "8px", padding: "12px 14px", marginBottom: "1rem" },
  resultRow: { display: "flex", justifyContent: "space-between", alignItems: "center", padding: "9px 0", borderBottom: "1px solid #1e293b", fontSize: "13px" },
  resultLabel: { fontFamily: "'DM Sans', sans-serif", color: "#475569" },
  resultVal: { fontFamily: "'DM Sans', sans-serif", fontWeight: "600" },
  infoCol: { display: "flex", flexDirection: "column", gap: "1rem", flex: "1 1 280px", maxWidth: "340px" },
  infoBox: { background: "#0f172a", border: "1px solid #1f2937", borderRadius: "14px", padding: "2rem" },
  infoTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "16px", fontWeight: "700", color: "#f1f5f9", marginBottom: "1.5rem" },
  infoSteps: { display: "flex", flexDirection: "column", gap: "1.5rem" },
  infoStep: { display: "flex", gap: "1rem", alignItems: "flex-start" },
  infoNum: { width: "28px", height: "28px", borderRadius: "50%", background: "rgba(220,38,38,0.1)", border: "1px solid rgba(239,68,68,0.2)", color: "#f87171", fontSize: "12px", fontWeight: "700", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontFamily: "'DM Sans', sans-serif" },
  infoStepTitle: { fontFamily: "'DM Sans', sans-serif", fontSize: "14px", fontWeight: "600", color: "#e2e8f0", marginBottom: "4px" },
  infoStepText: { fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#64748b", lineHeight: "1.7", fontWeight: "300" },
  warningBox: { background: "rgba(202,138,4,0.05)", border: "1px solid rgba(202,138,4,0.15)", borderRadius: "12px", padding: "1rem 1.1rem", display: "flex", gap: "0.75rem", alignItems: "flex-start" },
  warningText: { fontFamily: "'DM Sans', sans-serif", fontSize: "12px", color: "#64748b", lineHeight: "1.7" },
  footer: { background: "#060d1a", borderTop: "1px solid #1f2937", padding: "2rem", textAlign: "center", display: "flex", flexDirection: "column", gap: "6px", alignItems: "center" },
  footerLogo: { fontFamily: "'DM Sans', sans-serif", fontSize: "15px", fontWeight: "700", color: "#e2e8f0" },
  footerText: { fontFamily: "'DM Sans', sans-serif", fontSize: "13px", color: "#334155" },
};

export default DetectLeak;




