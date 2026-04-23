import React, { useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [countersDone, setCountersDone] = useState(false);
  const statsRef = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) entry.target.classList.add("in-view");
        });
      },
      { threshold: 0.12 }
    );
    document.querySelectorAll(".animate-section").forEach((el) => observer.observe(el));

    const statsObserver = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !countersDone) {
          animateCounters();
          setCountersDone(true);
        }
      },
      { threshold: 0.4 }
    );
    if (statsRef.current) statsObserver.observe(statsRef.current);

    return () => { observer.disconnect(); statsObserver.disconnect(); };
  }, [countersDone]);

  const animateCounters = () => {
    const counters = document.querySelectorAll(".stat-num[data-target]");
    counters.forEach((el) => {
      const target = el.getAttribute("data-target");
      const isFloat = target.includes(".");
      const numeric = parseFloat(target);
      const duration = 1800;
      const start = performance.now();
      const update = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = numeric * eased;
        el.textContent =
          (isFloat ? value.toFixed(1) : Math.round(value)) +
          el.getAttribute("data-suffix");
        if (progress < 1) requestAnimationFrame(update);
      };
      requestAnimationFrame(update);
    });
  };

  return (
    <div style={styles.container}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }

        @keyframes fadeUp {
          from { opacity: 0; transform: translateY(28px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes scanLine {
          0%   { top: 0%; opacity: 1; }
          90%  { top: 100%; opacity: 1; }
          100% { top: 100%; opacity: 0; }
        }
        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 0 0 rgba(59,130,246,0.4); }
          50%       { box-shadow: 0 0 0 10px rgba(59,130,246,0); }
        }
        @keyframes floatCard {
          0%, 100% { transform: translateY(0px); }
          50%       { transform: translateY(-6px); }
        }
        @keyframes glowBorder {
          0%, 100% { border-color: rgba(59,130,246,0.3); }
          50%       { border-color: rgba(59,130,246,0.7); }
        }

        .hero-badge { animation: fadeUp 0.55s cubic-bezier(.22,.68,0,1.2) 0.05s both; }
        .hero-title { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.2s  both; }
        .hero-sub   { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.38s both; }
        .hero-btn   { animation: fadeUp 0.65s cubic-bezier(.22,.68,0,1.2) 0.52s both; }
        .hero-card  { animation: fadeUp 0.75s cubic-bezier(.22,.68,0,1.2) 0.65s both; }

        .animate-section {
          opacity: 0; transform: translateY(36px);
          transition: opacity 0.75s ease, transform 0.75s ease;
        }
        .animate-section.in-view { opacity: 1; transform: translateY(0); }

        .feature-card {
          background: #0a1628;
          border: 1px solid #1e3a5f;
          border-radius: 16px;
          padding: 2rem;
          transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
          position: relative; overflow: hidden;
        }
        .feature-card::before {
          content: '';
          position: absolute; top: 0; left: 0; right: 0; height: 2px;
          background: linear-gradient(90deg, transparent, #3b82f6, transparent);
          opacity: 0; transition: opacity 0.3s ease;
        }
        .feature-card:hover { transform: translateY(-5px); border-color: rgba(59,130,246,0.5); box-shadow: 0 12px 40px rgba(29,78,216,0.15); }
        .feature-card:hover::before { opacity: 1; }

        .step-card {
          background: #0a1628;
          border: 1px solid #1e3a5f;
          border-radius: 16px;
          padding: 2rem 1.75rem;
          flex: 1 1 220px;
          max-width: 280px;
          transition: transform 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease;
        }
        .step-card:hover { transform: translateY(-4px); border-color: rgba(59,130,246,0.5); box-shadow: 0 12px 40px rgba(29,78,216,0.15); }

        .cta-card { transition: transform 0.3s ease, box-shadow 0.3s ease; }
        .cta-card:hover { transform: translateY(-5px); }

        .btn-primary {
          display: inline-block;
          padding: 15px 40px;
          background: #16a34a;
          color: white;
          border-radius: 10px;
          font-size: 16px; font-weight: 600;
          text-decoration: none;
          border: 1px solid #22c55e;
          margin-bottom: 4rem;
          letter-spacing: 0.02em;
          transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
          font-family: 'DM Sans', sans-serif;
          box-shadow: 0 4px 20px rgba(22,163,74,0.3);
        }
        .btn-primary:hover { background: #15803d; transform: translateY(-2px); box-shadow: 0 8px 28px rgba(22,163,74,0.45); }
        .btn-primary:active { transform: translateY(0); }

        .scan-line {
          position: absolute; left: 0; right: 0; height: 2px;
          background: linear-gradient(90deg, transparent, rgba(59,130,246,0.8), transparent);
          animation: scanLine 2.5s ease-in-out infinite;
        }
        .status-dot-live { animation: pulse 2s ease-in-out infinite; border-radius: 50%; }
        .floating-card   { animation: floatCard 4s ease-in-out infinite; }
        .glow-border     { animation: glowBorder 2.5s ease-in-out infinite; }

        .stat-bar {
          height: 3px;
          background: linear-gradient(90deg, #1d4ed8, #3b82f6);
          border-radius: 2px; transform-origin: left; transform: scaleX(0);
          transition: transform 1.2s cubic-bezier(.22,.68,0,1.2);
        }
        .animate-section.in-view .stat-bar { transform: scaleX(1); }

        .stats-row {
          display: flex; justify-content: center; align-items: center;
          width: 100%; max-width: 900px; margin: 0 auto;
        }
        .stat-item { flex: 1; text-align: center; padding: 0 1rem; min-width: 0; }
        .stat-divider { width: 1px; height: 56px; background: #1e3a5f; flex-shrink: 0; }
        .stat-num-text { white-space: nowrap; }

        .feature-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 20px; margin-top: 2.5rem;
        }

        .steps-row {
          display: flex; justify-content: center; align-items: stretch;
          gap: 0; margin-top: 2.5rem;
        }
        .step-connector {
          display: flex; align-items: center;
          padding: 0 8px; flex-shrink: 0;
        }

        .link-hover { transition: color 0.2s ease; }
        .link-hover:hover { color: #60a5fa !important; }

        @media (max-width: 640px) {
          .feature-grid { grid-template-columns: 1fr; }
          .steps-row { flex-direction: column; align-items: center; }
          .step-connector { display: none; }
          .stats-row { flex-wrap: wrap; gap: 2rem; }
          .stat-divider { display: none; }
        }
      `}</style>

      {/* ══ HERO ══ */}
      <section style={styles.hero}>
        <div style={styles.heroBg}>
          <div style={styles.gridOverlay}></div>
          <div style={styles.heroGlow1}></div>
          <div style={styles.heroGlow2}></div>
        </div>
        <div style={styles.heroContent}>
          <div className="hero-badge" style={styles.badge}>
            <span style={styles.badgeDot} className="status-dot-live"></span>
            AI-Powered Forensic Watermarking
          </div>
          <h1 className="hero-title" style={styles.heroTitle}>
            Stop Piracy.<br />
            <span style={styles.heroAccent}>Trace Every Leak.</span>
          </h1>
          <p className="hero-sub" style={styles.heroSub}>
            SentinelMark embeds an invisible identity into your videos.
            If it leaks — we find who did it. Instantly.
          </p>
          <div className="hero-btn">
            <Link to="/register" className="btn-primary">Get Protected →</Link>
          </div>
          <div className="hero-card floating-card" style={{ width: "100%", maxWidth: "460px" }}>
            <div style={styles.visualCard} className="glow-border">
              <div style={styles.visualTop}>
                <div style={{ display: "flex", gap: "6px" }}>
                  {["#ff5f57","#febc2e","#28c840"].map((c,i) => <div key={i} style={{ width:"11px", height:"11px", borderRadius:"50%", background:c }}></div>)}
                </div>
                <span style={styles.visualTitle}>sentinelmark — forensic-analyzer</span>
              </div>
              <div style={{ position: "relative", overflow: "hidden" }}>
                <div className="scan-line"></div>
                <div style={styles.visualBody}>
                  {[
                    { label: "Status",         val: "Analyzing...",  color: "#facc15" },
                    { label: "Source",         val: "Sony Liv",      color: "#f1f5f9" },
                    { label: "Confidence",     val: "97.4%",         color: "#22c55e" },
                    { label: "Distributor ID", val: "DIST-SL-00421", color: "#f1f5f9" },
                    { label: "Detected In",    val: "< 2 seconds",   color: "#60a5fa" },
                  ].map((row, i) => (
                    <div key={i} style={styles.visualRow}>
                      <span style={styles.visualLabel}>{row.label}</span>
                      <span style={{ ...styles.visualVal, color: row.color }}>{row.val}</span>
                    </div>
                  ))}
                  <div style={{ display:"flex", alignItems:"center", gap:"8px", marginTop:"14px", fontSize:"13px", color:"#22c55e", fontWeight:"600" }}>
                    <span style={{ width:"7px", height:"7px", borderRadius:"50%", background:"#22c55e", display:"inline-block" }}></span>
                    Leak source identified
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ══ STATS ══ */}
      <section style={styles.statsSection} ref={statsRef}>
        <div className="animate-section stats-row">
          {[
            { num:"99.8", suffix:"%",   label:"Detection Accuracy", target:"99.8" },
            { num:"<2s",               label:"Source Identified",   noCounter:true },
            { num:"0",   suffix:"%",   label:"Quality Loss",        target:"0" },
            { num:"256", suffix:"-bit",label:"Encryption",          target:"256" },
          ].map((s, i) => (
            <React.Fragment key={i}>
              <div className="stat-item">
                {s.noCounter
                  ? <div style={styles.statNum} className="stat-num-text">{s.num}</div>
                  : <div className="stat-num stat-num-text" style={styles.statNum} data-target={s.num} data-suffix={s.suffix}>{s.num}{s.suffix}</div>
                }
                <div style={styles.statLabel}>{s.label}</div>
                <div style={{ marginTop:"10px" }} className="stat-bar"></div>
              </div>
              {i < 3 && <div className="stat-divider" />}
            </React.Fragment>
          ))}
        </div>
      </section>

      {/* ══ FEATURES ══ */}
      <section style={styles.featuresSection}>
        <div style={styles.sectionInner}>
          <div className="animate-section">
            <p style={styles.sectionLabel}>CAPABILITIES</p>
            <h2 style={styles.sectionTitle}>Enterprise-grade protection</h2>
            <p style={styles.sectionSubtitle}>Built for studios, broadcasters, and content owners who can't afford leaks.</p>
          </div>
          <div className="feature-grid">
            {[
              { icon:"🛡️", title:"Invisible Watermarking", text:"Pixel-level tagging with zero visual impact. Survives re-encoding, compression, and screen capture." },
              { icon:"🔍", title:"Instant Detection",      text:"Upload any leaked video. We identify the source distributor in under 2 seconds." },
              { icon:"⚡", title:"Early Warning System",   text:"Flags suspicious distributor activity before a leak happens — giving you time to act." },
              { icon:"🌐", title:"Piracy Intelligence",    text:"Real-time tracking of every unauthorized share across the web, as it happens." },
            ].map((f, i) => (
              <div key={i} className="feature-card animate-section" style={{ transitionDelay:`${i*0.08}s` }}>
                <div style={styles.featureIconWrap}><span style={{ fontSize:"22px" }}>{f.icon}</span></div>
                <h3 style={styles.featureTitle}>{f.title}</h3>
                <p style={styles.featureText}>{f.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ══ HOW IT WORKS ══ */}
      <section style={styles.howSection}>
        <div style={styles.sectionInner}>
          <div className="animate-section" style={{ textAlign:"center" }}>
            <p style={styles.sectionLabel}>WORKFLOW</p>
            <h2 style={styles.sectionTitle}>From protection to detection in 3 steps</h2>
          </div>
          <div className="steps-row">
            {[
              { num:"01", icon:"🎬", title:"Register Asset",   text:"Upload your video. We embed a unique invisible watermark tied to every distributor in your chain." },
              { num:"02", icon:"📤", title:"Distribute Safely", text:"Share your content with confidence. Every copy carries a unique traceable forensic identity." },
              { num:"03", icon:"🎯", title:"Detect Any Leak",   text:"If a leak appears anywhere online, upload it. We reveal the exact source distributor instantly." },
            ].map((s, i) => (
              <React.Fragment key={i}>
                <div className="step-card animate-section" style={{ transitionDelay:`${i*0.12}s` }}>
                  <div style={styles.stepNum}>{s.num}</div>
                  <div style={{ fontSize:"28px", marginBottom:"0.9rem" }}>{s.icon}</div>
                  <h3 style={styles.stepTitle}>{s.title}</h3>
                  <p style={styles.stepText}>{s.text}</p>
                </div>
                {i < 2 && (
                  <div className="step-connector">
                    <div style={{ width:"28px", height:"1px", background:"#1e3a5f" }}></div>
                    <div style={{ fontSize:"18px", color:"#334155" }}>›</div>
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </section>
{/* ══ CTA ══ */}
<section style={styles.ctaSection}>
  <div style={styles.sectionInner}>
    <div className="animate-section" style={{ textAlign: "center" }}>
      <h2 style={styles.ctaTitle}>Protect your content today</h2>
      <p style={styles.ctaSub}>
        Choose your action and get started in seconds.
      </p>
    </div>

    <div
      style={{
        display: "grid", // 🔥 changed from flex
        gridTemplateColumns: "repeat(2, 1fr)", // 🔥 force 2x2
        gap: "20px",
        maxWidth: "700px",
        margin: "0 auto",
      }}
    >
      {[
        {
          border: "1px solid rgba(29,78,216,0.6)",
          shadow: "0 0 40px rgba(29,78,216,0.18)",
          icon: "🎬",
          badge: "Most Popular",
          badgeBg: "rgba(29,78,216,0.2)",
          badgeColor: "#93c5fd",
          title: "Register Asset",
          text: "Watermark and protect your video from piracy with military-grade forensic embedding.",
          btnBg: "#1d4ed8",
          btnBorder: "#3b82f6",
          btnColor: "white",
          btnText: "Register Now →",
          link: "/register",
        },

        {
          border: "1px solid #1e3a5f",
          shadow: "none",
          icon: "🕵️",
          badge: null,
          title: "Detect Leak",
          text: "Find the exact source of any leaked video instantly using our AI watermark analysis engine.",
          btnBg: "rgba(239,68,68,0.12)",
          btnBorder: "rgba(239,68,68,0.4)",
          btnColor: "#f87171",
          btnText: "Detect Source →",
          link: "/detect",
        },

        {
          border: "1px solid #1e3a5f",
          shadow: "none",
          icon: "🧪",
          badge: null,
          title: "Honeypot",
          text: "Deploy decoy content to trap unauthorized distributors and monitor leak activity.",
          btnBg: "rgba(168,85,247,0.12)",
          btnBorder: "rgba(168,85,247,0.4)",
          btnColor: "#c084fc",
          btnText: "Create Honeypot →",
          link: "/honeypot",
        },

        {
          border: "1px solid #1e3a5f",
          shadow: "none",
          icon: "📊",
          badge: null,
          title: "Risk Monitor",
          text: "Track distributor behavior and detect suspicious activity before leaks occur.",
          btnBg: "rgba(34,197,94,0.12)",
          btnBorder: "rgba(34,197,94,0.4)",
          btnColor: "#4ade80",
          btnText: "View Dashboard →",
          link: "/risk",
        },
      ].map((c, i) => (
        <div
          key={i}
          className="cta-card animate-section"
          style={{
            background: "#0a1628",
            borderRadius: "16px",
            padding: "2rem",
            // ❌ removed width: "300px"
            textAlign: "left",
            border: c.border,
            boxShadow: c.shadow,
            transitionDelay: `${i * 0.12}s`,
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "1.1rem",
            }}
          >
            <span style={{ fontSize: "28px" }}>{c.icon}</span>
            {c.badge && (
              <span
                style={{
                  fontSize: "11px",
                  padding: "3px 12px",
                  borderRadius: "100px",
                  fontWeight: "600",
                  letterSpacing: "0.04em",
                  background: c.badgeBg,
                  color: c.badgeColor,
                }}
              >
                {c.badge}
              </span>
            )}
          </div>

          <h3 style={styles.ctaCardTitle}>{c.title}</h3>
          <p style={styles.ctaCardText}>{c.text}</p>

          <Link
            to={c.link}
            style={{
              display: "inline-block",
              padding: "12px 24px",
              background: c.btnBg,
              color: c.btnColor,
              border: `1px solid ${c.btnBorder}`,
              borderRadius: "8px",
              fontSize: "14px",
              textDecoration: "none",
              fontWeight: "600",
              fontFamily: "'DM Sans', sans-serif",
            }}
          >
            {c.btnText}
          </Link>
        </div>
      ))}
    </div>
  </div>
</section>

      {/* ══ FOOTER ══ */}
      <footer style={styles.footer}>
        <div style={styles.footerInner}>
          <div style={{ display:"flex", flexDirection:"column", gap:"4px" }}>
            <span style={styles.footerLogo}>🛡️ SentinelMark</span>
            <span style={styles.footerTagline}>The future of anti-piracy intelligence</span>
          </div>
          <div style={{ display:"flex", gap:"1.5rem" }}>
            {["Privacy","Terms","Contact"].map((l) => (
              <span key={l} className="link-hover" style={styles.footerLink}>{l}</span>
            ))}
          </div>
        </div>
        <div style={styles.footerDivider}></div>
        <p style={styles.footerCopy}>© 2025 SentinelMark. All rights reserved.</p>
      </footer>
    </div>
  );
}

const styles = {
  container: { fontFamily:"'DM Sans', sans-serif", color:"white", background:"#070d1b" },

  hero: { minHeight:"100vh", display:"flex", flexDirection:"column", justifyContent:"center", alignItems:"center", position:"relative", overflow:"hidden", background:"linear-gradient(180deg, #0a1628 0%, #070d1b 100%)", borderBottom:"2px solid #1e3a5f" },
  heroBg: { position:"absolute", inset:0, zIndex:0 },
  gridOverlay: { position:"absolute", inset:0, backgroundImage:"linear-gradient(rgba(59,130,246,0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(59,130,246,0.06) 1px, transparent 1px)", backgroundSize:"60px 60px" },
  heroGlow1: { position:"absolute", top:"20%", left:"50%", transform:"translateX(-50%)", width:"700px", height:"450px", background:"radial-gradient(ellipse, rgba(29,78,216,0.2) 0%, transparent 70%)", pointerEvents:"none" },
  heroGlow2: { position:"absolute", bottom:"10%", right:"5%", width:"350px", height:"350px", background:"radial-gradient(ellipse, rgba(22,163,74,0.08) 0%, transparent 70%)", pointerEvents:"none" },

  heroContent: { position:"relative", zIndex:1, display:"flex", flexDirection:"column", alignItems:"center", textAlign:"center", padding:"5rem 2rem 4rem" },
  badge: { display:"inline-flex", alignItems:"center", gap:"8px", background:"rgba(29,78,216,0.15)", border:"1px solid rgba(59,130,246,0.35)", color:"#93c5fd", fontSize:"13px", padding:"7px 20px", borderRadius:"100px", marginBottom:"2rem", letterSpacing:"0.03em", fontWeight:"500", fontFamily:"'DM Sans', sans-serif" },
  badgeDot: { width:"7px", height:"7px", background:"#3b82f6", display:"inline-block" },

  heroTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"clamp(42px, 7vw, 72px)", fontWeight:"700", lineHeight:"1.08", marginBottom:"1.5rem", color:"#ffffff", letterSpacing:"-0.025em" },
  heroAccent: { color:"#3b82f6", display:"block" },
  heroSub: { fontFamily:"'DM Sans', sans-serif", fontSize:"18px", color:"#cbd5e1", maxWidth:"500px", lineHeight:"1.8", marginBottom:"2.5rem", fontWeight:"400" },

  visualCard: { background:"#0a1628", border:"1px solid rgba(59,130,246,0.3)", borderRadius:"14px", overflow:"hidden", textAlign:"left", position:"relative" },
  visualTop: { background:"#0f1f3d", padding:"12px 16px", display:"flex", alignItems:"center", gap:"10px", borderBottom:"1px solid #1e3a5f" },
  visualTitle: { fontSize:"12px", color:"#64748b", marginLeft:"6px", fontFamily:"'DM Sans', sans-serif", letterSpacing:"0.02em" },
  visualBody: { padding:"1.25rem" },
  visualRow: { display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 0", borderBottom:"1px solid #1e3a5f", fontSize:"13px" },
  visualLabel: { color:"#94a3b8", fontWeight:"400", fontFamily:"'DM Sans', sans-serif" },
  visualVal: { fontWeight:"600", fontFamily:"'DM Sans', sans-serif" },

  statsSection: { background:"#03060d", borderTop:"2px solid #1e3a5f", borderBottom:"2px solid #1e3a5f", padding:"4rem 2rem" },
  statNum: { fontFamily:"'DM Sans', sans-serif", fontSize:"28px", fontWeight:"700", color:"#60a5fa", letterSpacing:"-0.01em", whiteSpace:"nowrap" },
  statLabel: { fontFamily:"'DM Sans', sans-serif", fontSize:"12px", color:"#64748b", marginTop:"5px", letterSpacing:"0.08em", textTransform:"uppercase", fontWeight:"500" },

  featuresSection: { background:"linear-gradient(180deg, #0d1f3c 0%, #091428 100%)", padding:"7rem 2rem", borderBottom:"2px solid #1e3a5f" },
  sectionInner: { maxWidth:"980px", margin:"0 auto" },
  sectionLabel: { fontFamily:"'DM Sans', sans-serif", fontSize:"11px", letterSpacing:"0.2em", color:"#3b82f6", marginBottom:"0.75rem", fontWeight:"700" },
  sectionTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"clamp(28px, 4vw, 38px)", fontWeight:"700", color:"#ffffff", marginBottom:"0.75rem", lineHeight:"1.2", letterSpacing:"-0.01em" },
  sectionSubtitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"16px", color:"#94a3b8", fontWeight:"400", maxWidth:"520px" },
  featureIconWrap: { width:"48px", height:"48px", borderRadius:"12px", background:"rgba(29,78,216,0.15)", border:"1px solid rgba(59,130,246,0.2)", display:"flex", alignItems:"center", justifyContent:"center", marginBottom:"1.25rem" },
  featureTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"17px", fontWeight:"600", color:"#f1f5f9", marginBottom:"0.6rem" },
  featureText: { fontFamily:"'DM Sans', sans-serif", fontSize:"14px", color:"#94a3b8", lineHeight:"1.75", fontWeight:"400" },

  howSection: { background:"#03060d", padding:"7rem 2rem", borderBottom:"2px solid #1e3a5f" },
  stepNum: { fontFamily:"'DM Sans', sans-serif", fontSize:"11px", fontWeight:"700", color:"#3b82f6", background:"rgba(29,78,216,0.15)", border:"1px solid rgba(59,130,246,0.3)", display:"inline-block", padding:"4px 12px", borderRadius:"100px", marginBottom:"1.1rem", letterSpacing:"0.1em" },
  stepTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"17px", fontWeight:"600", color:"#f1f5f9", marginBottom:"0.6rem" },
  stepText: { fontFamily:"'DM Sans', sans-serif", fontSize:"14px", color:"#94a3b8", lineHeight:"1.75", fontWeight:"400" },

  ctaSection: { background:"linear-gradient(180deg, #0d1f3c 0%, #070d1b 100%)", padding:"7rem 2rem 8rem", textAlign:"center" },
  ctaTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"clamp(28px, 4vw, 38px)", fontWeight:"700", color:"#ffffff", marginBottom:"0.75rem", letterSpacing:"-0.01em" },
  ctaSub: { fontFamily:"'DM Sans', sans-serif", fontSize:"16px", color:"#94a3b8", marginBottom:"3rem", fontWeight:"400" },
  ctaCardTitle: { fontFamily:"'DM Sans', sans-serif", fontSize:"20px", fontWeight:"700", color:"#ffffff", marginBottom:"0.6rem" },
  ctaCardText: { fontFamily:"'DM Sans', sans-serif", fontSize:"14px", color:"#94a3b8", marginBottom:"1.75rem", lineHeight:"1.75", fontWeight:"400" },

  footer: { background:"#02040a", borderTop:"1px solid #1e3a5f", padding:"2.5rem 2rem 2rem" },
  footerInner: { display:"flex", justifyContent:"space-between", alignItems:"center", flexWrap:"wrap", gap:"1rem", maxWidth:"980px", margin:"0 auto", paddingBottom:"1.5rem" },
  footerLogo: { fontFamily:"'DM Sans', sans-serif", fontSize:"16px", fontWeight:"700", color:"#e2e8f0" },
  footerTagline: { fontFamily:"'DM Sans', sans-serif", fontSize:"13px", color:"#475569" },
  footerLink: { fontFamily:"'DM Sans', sans-serif", fontSize:"13px", color:"#64748b", cursor:"pointer" },
  footerDivider: { height:"1px", background:"#1e3a5f", maxWidth:"980px", margin:"0 auto 1.5rem" },
  footerCopy: { fontFamily:"'DM Sans', sans-serif", fontSize:"12px", color:"#334155", textAlign:"center" },
};

export default Home;


