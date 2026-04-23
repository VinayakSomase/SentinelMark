
import { Link, useLocation } from "react-router-dom";

const navLinks = [
  { label: "Home", to: "/" },
  { label: "Register Asset", to: "/register" },
  { label: "Detect Leak", to: "/detect" },
  { label: "Honeypot", to: "/honeypot" },
  { label: "Risk Monitor", to: "/risk" },
];

function Navbar() {
  const location = useLocation();

  return (
    <nav style={styles.nav}>
      <div style={styles.navInner}>
        
        {/* LEFT: LOGO */}
        <Link to="/" style={styles.logo}>
          <span style={styles.logoIcon}>🛡️</span>
          <div>
            <div style={styles.logoText}>SentinelMark</div>
            <div style={styles.logoSub}>ANTI-PIRACY INTELLIGENCE</div>
          </div>
        </Link>

        {/* RIGHT SIDE */}
        <div style={styles.navRight}>
          {navLinks.map((link) => {
            const isActive =
              link.to === "/"
                ? location.pathname === "/"
                : location.pathname.startsWith(link.to);

            return (
              <Link
                key={link.to}
                to={link.to}
                style={{
                  ...styles.navLink,
                  ...(isActive ? styles.navLinkActive : {}),
                }}
              >
                {link.label}
                {isActive && <span style={styles.activeDot} />}
              </Link>
            );
          })}
        </div>

      </div>
    </nav>
  );
}

const styles = {
  nav: {
    position: "fixed",
    top: 0,
    left: 0,
    right: 0,
    zIndex: 1000,
    background: "rgba(8, 10, 20, 0.85)",
    backdropFilter: "blur(12px)",
    borderBottom: "1px solid rgba(255,255,255,0.06)",
    fontFamily: "'DM Sans', sans-serif",
  },

  navInner: {
    width: "100%",                  // ✅ full width
    display: "flex",
    alignItems: "center",
    padding: "0 16px",              // smaller padding
    height: "64px",
    boxSizing: "border-box",
  },

  logo: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    textDecoration: "none",
    flexShrink: 0,
  },

  logoIcon: { fontSize: "20px" },

  logoText: {
    fontFamily: "'Syne', sans-serif",
    fontSize: "16px",
    fontWeight: "700",
    color: "#ffffff",
  },

  logoSub: {
    fontSize: "9px",
    color: "#3b82f6",
    letterSpacing: "0.08em",
  },

  /* 🔥 RIGHT ALIGN FIX */
  navRight: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
    marginLeft: "auto",   // ✅ pushes fully right
    paddingRight: "4px",  // ✅ tiny edge spacing
  },

  navLink: {
    padding: "8px 12px",
    borderRadius: "8px",
    fontSize: "14px",
    color: "rgba(255,255,255,0.6)",
    textDecoration: "none",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: "4px",
    whiteSpace: "nowrap",
  },

  navLinkActive: {
    color: "#ffffff",
    background: "rgba(59, 130, 246, 0.15)",
    border: "1px solid rgba(59, 130, 246, 0.3)",
  },

  activeDot: {
    width: "4px",
    height: "4px",
    borderRadius: "50%",
    background: "#3b82f6",
  },
};

export default Navbar;

