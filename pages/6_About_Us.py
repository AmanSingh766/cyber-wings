import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, sidebar_logo

st.set_page_config(page_title="About Us — CyberWings", page_icon="👥", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#00ff88; text-shadow:0 0 25px rgba(0,255,136,0.5); letter-spacing:2px;">
        👥 ABOUT CYBER WINGS
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#007744; font-size:0.9rem; margin-top:6px;">
        The Team Behind the Shield
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#00ff88,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

# ─── LOGO / MISSION ──────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin:30px 0 20px 0;">
    <div style="display:inline-block; background:linear-gradient(135deg,#050f1a,#081a2e);
                border:2px solid #00d4ff44; border-radius:24px; padding:30px 60px;
                box-shadow:0 0 60px rgba(0,212,255,0.12);">
        <div style="font-size:4rem; margin-bottom:8px; filter:drop-shadow(0 0 20px #00d4ff);">🛡️</div>
        <div style="font-family:'Orbitron',monospace; font-size:2.5rem; font-weight:900;
                    color:#00d4ff; text-shadow:0 0 30px rgba(0,212,255,0.7); letter-spacing:4px;">
            CYBER WINGS
        </div>
        <div style="font-family:'Share Tech Mono',monospace; color:#0077aa; font-size:0.95rem;
                    margin-top:8px; letter-spacing:2px;">
            WEB VULNERABILITY INTELLIGENCE PLATFORM
        </div>
        <div style="width:150px; height:1px; background:linear-gradient(90deg,transparent,#00d4ff,transparent);
                    margin:16px auto;"></div>
        <div style="font-family:'Rajdhani',sans-serif; color:#4488aa; font-size:1rem;
                    max-width:450px; line-height:1.6;">
            Empowering developers and security researchers to identify and 
            remediate web vulnerabilities before attackers do.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── MISSION / VISION ────────────────────────────────────────────────────────
mc1, mc2, mc3 = st.columns(3)
for col, icon, title, desc in zip(
    [mc1, mc2, mc3],
    ["🎯", "👁️", "⚡"],
    ["Our Mission", "Our Vision", "Our Approach"],
    [
        "Build accessible, open-source cybersecurity tools that help developers and organizations proactively identify vulnerabilities and secure their web applications.",
        "A safer internet where every developer can easily identify and fix security flaws before malicious actors exploit them. Security for everyone.",
        "Combining automated scanning with detailed educational content — so you don't just know if you're vulnerable, but understand WHY and HOW to fix it.",
    ]
):
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#070e1d,#0c1a2e);
                    border:1px solid #0d3a5a; border-radius:14px; padding:22px 18px;
                    text-align:center; height:100%;">
            <div style="font-size:2rem; margin-bottom:10px;">{icon}</div>
            <div style="font-family:'Orbitron',monospace; color:#00aaff; font-size:0.9rem;
                        font-weight:700; margin-bottom:12px; letter-spacing:1px;">{title.upper()}</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#4488aa; font-size:0.95rem;
                        line-height:1.6;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)

# ─── TEAM SECTION ────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; font-family:'Orbitron',monospace; font-size:1.4rem;
            color:#00aaff; margin:20px 0 30px 0; letter-spacing:2px;">
    👨‍💻 MEET THE TEAM
</div>
""", unsafe_allow_html=True)

TEAM = [
    {
        "name":    "Rahul Solanki",
        "role":    "Full Stack Developer",
        "emoji":   "🚀",
        "color":   "#00d4ff",
        "contrib": "Led the complete architecture and development of the platform — from backend scanner engines to frontend UI design. Responsible for core vulnerability detection logic, Streamlit integration, and ensuring the platform runs seamlessly end-to-end.",
        "tags":    ["Python", "Streamlit", "Security", "Architecture"],
        "contrib_pct": 100,
    },
    {
        "name":    "Aman Singh",
        "role":    "Backend Developer",
        "emoji":   "⚙️",
        "color":   "#0088ff",
        "contrib": "Built and optimized the vulnerability scanning engines including SQL injection, XSS, and CSRF detection modules. Developed robust request handling, payload management, and response analysis pipelines for reliable scanning.",
        "tags":    ["Backend", "Scanner Engines", "Python", "APIs"],
        "contrib_pct": 75,
    },
    {
        "name":    "Kuldip Jadav",
        "role":    "UI/UX Designer",
        "emoji":   "🎨",
        "color":   "#aa44ff",
        "contrib": "Designed the Cyber Blue visual identity and user experience of the platform. Created wireframes, color schemes, and the immersive dark-themed interface that makes complex security data clear and accessible to all users.",
        "tags":    ["UI Design", "CSS", "User Experience", "Branding"],
        "contrib_pct": 55,
    },
    {
        "name":    "Harshit Singhal",
        "role":    "Security Analyst & QA",
        "emoji":   "🔐",
        "color":   "#ff8800",
        "contrib": "Curated the security payload libraries, validated scanner accuracy, and performed manual penetration testing to verify findings. Ensured all vulnerability detection logic aligns with OWASP standards and real-world attack vectors.",
        "tags":    ["Penetration Testing", "OWASP", "QA", "Security Research"],
        "contrib_pct": 40,
    },
    {
        "name":    "Swayam Shah",
        "role":    "Research & Documentation",
        "emoji":   "📚",
        "color":   "#00ff88",
        "contrib": "Researched the latest CVEs, vulnerability databases, and cybersecurity literature to inform scanner logic. Authored technical documentation, educational content, and the ethical use guidelines integrated throughout the platform.",
        "tags":    ["Research", "CVE Database", "Documentation", "Content"],
        "contrib_pct": 25,
    },
]

for i, member in enumerate(TEAM):
    bar_width = member["contrib_pct"]
    col_card, col_space = st.columns([5, 1])
    with col_card:
        tags_html = "".join([
            f'<span style="background:{member["color"]}15; color:{member["color"]}; '
            f'border:1px solid {member["color"]}44; padding:3px 10px; border-radius:12px; '
            f'font-size:0.75rem; font-family:Share Tech Mono,monospace; margin:3px; '
            f'display:inline-block;">{tag}</span>'
            for tag in member["tags"]
        ])
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#070e1d,#0c1a2e);
                    border:1px solid {member['color']}33;
                    border-left:4px solid {member['color']};
                    border-radius:0 14px 14px 0; padding:22px 26px; margin:10px 0;
                    box-shadow:0 4px 20px {member['color']}0d;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
                <div style="display:flex; align-items:center; gap:14px;">
                    <div style="font-size:2.2rem; background:{member['color']}18;
                                border:1px solid {member['color']}44; border-radius:12px;
                                padding:8px 12px; line-height:1;">{member['emoji']}</div>
                    <div>
                        <div style="font-family:'Orbitron',monospace; font-size:1.15rem; font-weight:700;
                                    color:{member['color']}; letter-spacing:1px;">{member['name']}</div>
                        <div style="font-family:'Share Tech Mono',monospace; color:#335577;
                                    font-size:0.82rem; margin-top:3px; letter-spacing:1px;">
                            {member['role'].upper()}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-family:'Share Tech Mono',monospace; color:#224466; font-size:0.72rem; margin-bottom:4px;">CONTRIBUTION</div>
                    <div style="background:#0a1525; border:1px solid #0d2a4a; border-radius:6px;
                                padding:3px; width:140px;">
                        <div style="background:linear-gradient(90deg, {member['color']}88, {member['color']});
                                    height:8px; border-radius:4px; width:{bar_width}%;"></div>
                    </div>
                </div>
            </div>
            <div style="font-family:'Rajdhani',sans-serif; color:#4477aa; font-size:0.95rem;
                        line-height:1.6; margin:14px 0 12px 0;">
                {member['contrib']}
            </div>
            <div>{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── TECH STACK ──────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; font-family:'Orbitron',monospace; font-size:1.2rem;
            color:#00aaff; margin:20px 0 24px 0; letter-spacing:2px;">
    🛠️ TECH STACK
</div>
""", unsafe_allow_html=True)

tech = [
    ("🐍", "Python 3.10+", "Core Language"),
    ("⚡", "Streamlit", "Web Framework"),
    ("🌐", "Requests", "HTTP Client"),
    ("🔒", "pyOpenSSL", "SSL Analysis"),
    ("🍜", "BeautifulSoup4", "HTML Parsing"),
    ("🔍", "Socket", "Port Scanning"),
]
tcols = st.columns(len(tech))
for col, (icon, name, desc) in zip(tcols, tech):
    with col:
        st.markdown(f"""
        <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                    border:1px solid #0d2a4a; border-radius:12px; padding:16px 8px;">
            <div style="font-size:1.8rem; margin-bottom:6px;">{icon}</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#00aaff; font-size:0.95rem;
                        font-weight:700;">{name}</div>
            <div style="font-family:'Share Tech Mono',monospace; color:#224466;
                        font-size:0.72rem; margin-top:3px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ─── FOOTER / LOCATION ───────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; background:linear-gradient(135deg,#050c1a,#080f1e);
            border:1px solid #0d2a4a; border-radius:16px; padding:30px 20px; margin-top:10px;">
    <div style="font-size:2.5rem; margin-bottom:12px;">📍</div>
    <div style="font-family:'Orbitron',monospace; font-size:1.2rem; color:#00d4ff;
                letter-spacing:2px; margin-bottom:8px;">OUR LOCATION</div>
    <div style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; color:#55aacc;
                font-weight:700;">Vadodara, Gujarat, India</div>
    <div style="font-family:'Share Tech Mono',monospace; color:#224466; font-size:0.8rem;
                margin-top:8px;">22.3072° N, 73.1812° E</div>
    <div style="width:120px; height:1px; background:linear-gradient(90deg,transparent,#00d4ff,transparent);
                margin:16px auto;"></div>
    <div style="font-family:'Rajdhani',sans-serif; color:#2a5570; font-size:0.9rem; line-height:1.7;">
        Built with ❤️ and a passion for cybersecurity.<br>
        <strong style="color:#335577;">Cyber Wings</strong> — Protecting the digital world, one vulnerability at a time.
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#1a3a5c; font-size:0.72rem;
                margin-top:16px; letter-spacing:2px;">
        © 2025 CYBER WINGS  •  VADODARA, GUJARAT  •  ALL RIGHTS RESERVED
    </div>
</div>
""", unsafe_allow_html=True)
