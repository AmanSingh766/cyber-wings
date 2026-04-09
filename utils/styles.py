def get_cyber_theme():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

    /* ── Background ── */
    .stApp {
        background-color: #050a15 !important;
        background-image:
            radial-gradient(ellipse at 20% 50%, rgba(0,100,255,0.05) 0%, transparent 55%),
            radial-gradient(ellipse at 80% 20%, rgba(0,212,255,0.05) 0%, transparent 55%);
    }

    /* Hide default header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060c1a 0%, #080f20 100%) !important;
        border-right: 1px solid #0d2a4a !important;
    }

    /* Sidebar nav links - clean, no overlap */
    [data-testid="stSidebarNav"] {
        padding-top: 0 !important;
    }
    [data-testid="stSidebarNav"] ul {
        padding: 0 8px !important;
    }
    [data-testid="stSidebarNav"] li {
        margin: 2px 0 !important;
    }
    [data-testid="stSidebarNav"] a {
        color: #5588aa !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 6px 12px !important;
        display: block !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    [data-testid="stSidebarNav"] a:hover {
        color: #00d4ff !important;
        background: rgba(0,212,255,0.08) !important;
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        color: #00d4ff !important;
        background: rgba(0,212,255,0.12) !important;
        border-left: 3px solid #00d4ff !important;
    }

    /* ── Main content text ── */
    .stMarkdown p {
        color: #b0c8e0 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    .stMarkdown li {
        color: #b0c8e0 !important;
        font-family: 'Rajdhani', sans-serif !important;
    }

    /* ── Headings ── */
    h1, .stMarkdown h1 {
        font-family: 'Orbitron', monospace !important;
        color: #00d4ff !important;
        text-shadow: 0 0 25px rgba(0,212,255,0.5);
        font-weight: 900 !important;
    }
    h2, .stMarkdown h2 {
        font-family: 'Orbitron', monospace !important;
        color: #00aaff !important;
    }
    h3, .stMarkdown h3 {
        font-family: 'Rajdhani', sans-serif !important;
        color: #0099dd !important;
        font-weight: 700 !important;
    }

    /* ── Table ── */
    .stMarkdown table {
        border-collapse: collapse !important;
        width: 100% !important;
    }
    .stMarkdown table th {
        background: #0a1525 !important;
        color: #00d4ff !important;
        font-family: 'Rajdhani', sans-serif !important;
        border: 1px solid #0d2a4a !important;
        padding: 8px 12px !important;
    }
    .stMarkdown table td {
        color: #88aacc !important;
        font-family: 'Rajdhani', sans-serif !important;
        border: 1px solid #0a1e35 !important;
        padding: 7px 12px !important;
        background: #070e1d !important;
    }

    /* ── Code blocks ── */
    .stMarkdown code {
        background: #0a1525 !important;
        color: #00d4ff !important;
        border: 1px solid #0d2a4a !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        font-family: 'Share Tech Mono', monospace !important;
    }
    .stMarkdown pre {
        background: #070e1d !important;
        border: 1px solid #0d2a4a !important;
        border-radius: 8px !important;
        padding: 14px !important;
    }
    .stMarkdown pre code {
        border: none !important;
        background: transparent !important;
        color: #55aacc !important;
    }

    /* ── Text Input ── */
    .stTextInput > div > div > input {
        background-color: #0a1525 !important;
        border: 1px solid #153555 !important;
        color: #00d4ff !important;
        border-radius: 8px !important;
        font-family: 'Share Tech Mono', monospace !important;
        font-size: 0.95rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 12px rgba(0,212,255,0.3) !important;
    }
    .stTextInput > label {
        color: #7aaacf !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #002a6e, #0055bb) !important;
        color: #00d4ff !important;
        border: 1px solid #0077dd !important;
        border-radius: 8px !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 0.7rem !important;
        font-weight: 700 !important;
        padding: 0.55rem 1.4rem !important;
        box-shadow: 0 0 15px rgba(0,100,255,0.25) !important;
        transition: all 0.3s ease !important;
        letter-spacing: 1px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #003a99, #00aaff) !important;
        box-shadow: 0 0 25px rgba(0,212,255,0.6) !important;
        color: #ffffff !important;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #080f1e !important;
        border-bottom: 1px solid #0d2a4a !important;
        gap: 4px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #4a7090 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 16px !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00d4ff !important;
        background: rgba(0,212,255,0.08) !important;
        border-bottom: 2px solid #00d4ff !important;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #060c1a !important;
        border: 1px solid #0d2a4a !important;
        border-radius: 0 8px 8px 8px !important;
        padding: 20px !important;
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
    }

    /* ── Progress ── */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #003399, #00d4ff) !important;
    }

    /* ── Expander ── */
    [data-testid="stExpander"] {
        background: #080f1e !important;
        border: 1px solid #0d2a4a !important;
        border-radius: 8px !important;
    }
    [data-testid="stExpanderToggleIcon"] {
        color: #00aaff !important;
    }

    /* ── Checkbox ── */
    .stCheckbox label {
        color: #7aaacf !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 0.95rem !important;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; background: #060c1a; }
    ::-webkit-scrollbar-thumb { background: #0d2a4a; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #0055aa; }

    /* ── Divider ── */
    hr { border-color: #0d2a4a !important; margin: 16px 0 !important; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #00d4ff !important; }
    </style>
    """


# def cyber_header(title, subtitle="", icon="🛡️"):
#     return f"""
#     <div style="text-align:center; padding: 30px 0 15px 0;">
#         <div style="font-family:'Orbitron',monospace; font-size:2.2rem; color:#00d4ff;
#                     text-shadow:0 0 30px rgba(0,212,255,0.7); font-weight:900; letter-spacing:2px;">
#             {icon} {title}
#         </div>
#         {f'<div style="font-family:\'Share Tech Mono\',monospace; color:#0077cc; font-size:1rem; margin-top:8px; letter-spacing:1px;">{subtitle}</div>' if subtitle else ''}
#         <div style="width:180px; height:2px; background:linear-gradient(90deg,transparent,#00d4ff,transparent); margin:15px auto 0 auto;"></div>
#     </div>
#     """
def cyber_header(title, subtitle="", icon="🛡️"):
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<div style="font-family:Share Tech Mono,monospace; color:#0077cc; font-size:1rem; margin-top:8px; letter-spacing:1px;">{subtitle}</div>'

    return f"""
    <div style="text-align:center; padding: 30px 0 15px 0;">
        <div style="font-family:'Orbitron',monospace; font-size:2.2rem; color:#00d4ff;
                    text-shadow:0 0 30px rgba(0,212,255,0.7); font-weight:900; letter-spacing:2px;">
            {icon} {title}
        </div>
        {subtitle_html}
        <div style="width:180px; height:2px; background:linear-gradient(90deg,transparent,#00d4ff,transparent); margin:15px auto 0 auto;"></div>
    </div>
    """


# def cyber_card(title, content, border_color="#0d2a4a", icon=""):
#     return f"""
#     <div style="background:linear-gradient(135deg,#080f1f,#0c1628);
#                 border:1px solid {border_color}; border-radius:12px;
#                 padding:20px; margin:10px 0;
#                 box-shadow:0 0 20px rgba(0,80,200,0.12);">
#         {f'<div style="font-family:\'Rajdhani\',sans-serif; font-size:1.15rem; font-weight:700; color:#00aaff; margin-bottom:10px;">{icon} {title}</div>' if title else ''}
#         <div style="color:#b0c8e0; font-family:\'Rajdhani\',sans-serif; font-size:1rem; line-height:1.6;">
#             {content}
#         </div>
#     </div>
#     """
def cyber_card(title, content, border_color="#0d2a4a", icon=""):
    title_html = ""
    if title:
        title_html = f'<div style="font-family:Rajdhani,sans-serif; font-size:1.15rem; font-weight:700; color:#00aaff; margin-bottom:10px;">{icon} {title}</div>'

    return f"""
    <div style="background:linear-gradient(135deg,#080f1f,#0c1628);
                border:1px solid {border_color}; border-radius:12px;
                padding:20px; margin:10px 0;
                box-shadow:0 0 20px rgba(0,80,200,0.12);">
        {title_html}
        <div style="color:#b0c8e0; font-family:Rajdhani,sans-serif; font-size:1rem; line-height:1.6;">
            {content}
        </div>
    </div>
    """


def status_badge(status, text):
    colors = {
        "safe":    ("#00ff88", "#001a0d"),
        "danger":  ("#ff4444", "#1a0000"),
        "warning": ("#ffcc00", "#1a1400"),
        "info":    ("#00d4ff", "#001a26"),
    }
    fg, bg = colors.get(status, ("#00d4ff", "#001a26"))
    return f"""<span style="background:{bg}; color:{fg}; border:1px solid {fg};
        padding:4px 14px; border-radius:20px; font-size:0.82rem; font-weight:700;
        font-family:'Share Tech Mono',monospace; letter-spacing:1px;">{text}</span>"""


def sidebar_logo():
    return """
    <div style="text-align:center; padding:18px 10px 12px 10px;">
        <div style="font-family:'Orbitron',monospace; font-size:1.3rem; color:#00d4ff;
                    text-shadow:0 0 15px rgba(0,212,255,0.6); font-weight:900; letter-spacing:1px;">
            🛡️ CYBER WINGS
        </div>
        <div style="font-family:'Share Tech Mono',monospace; color:#0077aa; font-size:0.68rem; margin-top:4px; letter-spacing:1px;">
            Web Vulnerability Scanner
        </div>
        <div style="width:110px; height:1px; background:linear-gradient(90deg,transparent,#00d4ff,transparent); margin:10px auto 4px auto;"></div>
    </div>
    """
