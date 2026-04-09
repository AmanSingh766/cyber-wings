import streamlit as st
import sys, os
import os
os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
# sys.path.insert(0, os.path.dirname(__file__))

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, cyber_card, sidebar_logo

st.set_page_config(
    page_title="CyberWings — Web Vulnerability Scanner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

# ─── HERO SECTION ────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:50px 0 10px 0;">
    <div style="display:inline-block; background:rgba(0,212,255,0.06);
                border:1px solid #0d3a6a; border-radius:20px; padding:8px 22px;
                font-family:'Share Tech Mono',monospace; color:#0099cc;
                font-size:0.8rem; letter-spacing:2px; margin-bottom:18px;">
        ⚡  ADVANCED CYBERSECURITY TOOLKIT  ⚡
    </div>
    <div style="font-family:'Orbitron',monospace; font-size:3.2rem; font-weight:900;
                color:#00d4ff; text-shadow:0 0 40px rgba(0,212,255,0.65);
                line-height:1.1; letter-spacing:3px;">
        🛡️ CYBER WINGS
    </div>
    <div style="font-family:'Rajdhani',sans-serif; color:#5599cc; font-size:1.25rem;
                margin-top:10px; letter-spacing:1px;">
        Web Vulnerability Intelligence Platform
    </div>
    <div style="width:250px; height:2px;
                background:linear-gradient(90deg,transparent,#00d4ff,transparent);
                margin:22px auto;"></div>
    <div style="font-family:'Rajdhani',sans-serif; color:#7799bb; font-size:1rem;
                max-width:600px; margin:0 auto; line-height:1.6;">
        Detect SSL weaknesses, SQL Injections, XSS, CSRF, Open Redirects,<br>
        Sensitive File Exposures, Port leaks & Security Header misconfigurations.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── QUICK STATS ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
stats = [
    ("6", "Vulnerability Modules", "🔍"),
    ("50+", "Attack Payloads", "💉"),
    ("20+", "Sensitive File Checks", "📂"),
    ("17", "Port Scans", "🌐"),
]
for col, (val, label, icon) in zip([col1, col2, col3, col4], stats):
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#070e1d,#0b1626);
                    border:1px solid #0d2a4a; border-radius:14px;
                    padding:22px 10px; text-align:center;
                    box-shadow:0 0 25px rgba(0,80,200,0.12);">
            <div style="font-size:1.8rem;">{icon}</div>
            <div style="font-family:'Orbitron',monospace; font-size:2rem;
                        color:#00d4ff; font-weight:900; text-shadow:0 0 15px rgba(0,212,255,0.5);">
                {val}
            </div>
            <div style="font-family:'Rajdhani',sans-serif; color:#5588aa;
                        font-size:0.9rem; margin-top:4px;">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ─── FEATURE CARDS ───────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; font-family:'Orbitron',monospace; font-size:1.4rem;
            color:#00aaff; margin-bottom:25px;">
    🔧 SCANNING MODULES
</div>
""", unsafe_allow_html=True)

modules = [
    {
        "icon": "🔒",
        "title": "SSL Certificate Analyzer",
        "desc": "Deep inspection of SSL/TLS certificates — expiry, cipher strength, TLS version, SANs, and grading.",
        "badge": "FOUNDATIONAL",
        "color": "#00d4ff",
        "page": "🔒_SSL_Certificate"
    },
    {
        "icon": "💉",
        "title": "SQL Injection Scanner",
        "desc": "Error-based and time-based blind SQLi detection across URL parameters using curated payloads.",
        "badge": "CRITICAL",
        "color": "#ff4444",
        "page": "💉_SQL_Injection"
    },
    {
        "icon": "⚡",
        "title": "XSS Scanner",
        "desc": "Reflected Cross-Site Scripting detection with CSP header analysis and 14+ injection vectors.",
        "badge": "HIGH RISK",
        "color": "#ffcc00",
        "page": "⚡_XSS_Scanner"
    },
    {
        "icon": "🛡️",
        "title": "CSRF Scanner",
        "desc": "Form token analysis, SameSite cookie auditing, and CORS misconfiguration detection.",
        "badge": "MEDIUM",
        "color": "#ff8800",
        "page": "🛡️_CSRF_Scanner"
    },
    {
        "icon": "🔍",
        "title": "Advanced Scanner",
        "desc": "Security headers audit, sensitive file exposure, open redirect testing, and port scanning.",
        "badge": "ADVANCED",
        "color": "#aa44ff",
        "page": "🔍_Advanced_Scanner"
    },
    {
        "icon": "👥",
        "title": "About Cyber Wings",
        "desc": "Meet the team behind this project — our mission, roles, and location in Vadodara, Gujarat.",
        "badge": "TEAM",
        "color": "#00ff88",
        "page": "👥_About_Us"
    },
]

rows = [modules[:3], modules[3:]]
for row in rows:
    cols = st.columns(3)
    for col, mod in zip(cols, row):
        with col:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,#070e1d,#0c1829);
                        border:1px solid {mod['color']}33;
                        border-top: 2px solid {mod['color']};
                        border-radius:12px; padding:22px 18px;
                        box-shadow:0 4px 20px {mod['color']}15;
                        height:100%; transition:all 0.3s ease;">
                <div style="font-size:2rem; margin-bottom:8px;">{mod['icon']}</div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                    <span style="font-family:'Rajdhani',sans-serif; font-size:1.05rem;
                                 font-weight:700; color:#ddeeff;">{mod['title']}</span>
                    <span style="background:{mod['color']}18; color:{mod['color']};
                                 border:1px solid {mod['color']}55; padding:2px 8px;
                                 border-radius:10px; font-size:0.65rem;
                                 font-family:'Share Tech Mono',monospace;">{mod['badge']}</span>
                </div>
                <div style="font-family:'Rajdhani',sans-serif; color:#5588aa;
                            font-size:0.95rem; line-height:1.55;">
                    {mod['desc']}
                </div>
                <div style="margin-top:14px; font-family:'Share Tech Mono',monospace;
                            color:{mod['color']}; font-size:0.75rem; opacity:0.7;">
                    → Use sidebar to navigate
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

# ─── DISCLAIMER ──────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)
st.markdown("""
<div style="background:rgba(255,100,0,0.05); border:1px solid #442200;
            border-radius:10px; padding:15px 20px; text-align:center;">
    <div style="font-family:'Orbitron',monospace; color:#ff8800;
                font-size:0.85rem; letter-spacing:1px; margin-bottom:6px;">
        ⚠️  ETHICAL USE DISCLAIMER
    </div>
    <div style="font-family:'Rajdhani',sans-serif; color:#886644; font-size:0.9rem; line-height:1.5;">
        This tool is intended <strong style="color:#ffaa55;">for educational and authorized testing purposes only.</strong><br>
        Scanning websites without explicit permission may be illegal. Always obtain proper authorization before testing.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-top:30px; font-family:'Share Tech Mono',monospace;
            color:#1a3a5c; font-size:0.75rem; letter-spacing:2px;">
    CYBER WINGS  •  VADODARA, GUJARAT  •  2025
</div>
""", unsafe_allow_html=True)
