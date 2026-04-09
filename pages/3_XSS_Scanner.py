import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, sidebar_logo
from utils.xss_checker import check_xss

st.set_page_config(page_title="XSS Scanner — CyberWings", page_icon="⚡", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#ffcc00; text-shadow:0 0 25px rgba(255,200,0,0.5); letter-spacing:2px;">
        ⚡ XSS VULNERABILITY SCANNER
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#aa8800; font-size:0.9rem; margin-top:6px;">
        Detect Cross-Site Scripting (Reflected XSS) Vulnerabilities
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#ffcc00,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

# ─── ABOUT XSS ───────────────────────────────────────────────────────────────
with st.expander("📖  What is Cross-Site Scripting (XSS)?  (Click to learn)", expanded=False):
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.markdown("""
        ### ⚡ Cross-Site Scripting (XSS)

        **XSS** is a client-side code injection attack where malicious scripts are injected into
        trusted web pages. It is ranked **#3 in OWASP Top 10**. When successful, the attacker
        can execute arbitrary JavaScript in a victim's browser.

        #### Types of XSS:
        | Type | How | Persistence |
        |------|-----|-------------|
        | **Reflected** | Payload in URL, echoed in response | Non-persistent |
        | **Stored** | Payload saved in DB, served to all users | Persistent (dangerous!) |
        | **DOM-Based** | Payload modifies DOM client-side | Non-persistent |
        | **Blind XSS** | Payload fires in admin panel / logs | Delayed |

        #### Classic Attack Scenario:
        1. Attacker crafts a malicious URL with JS payload
        2. Victim clicks the link (phishing, social engineering)
        3. Server reflects the payload without sanitization
        4. Victim's browser executes attacker's script
        5. Attacker steals session cookies → **Account takeover!**

        #### What XSS Can Do:
        - 🍪 **Cookie theft** — `document.cookie` exfiltration
        - ⌨️ **Keylogging** — Capture form inputs
        - 🔄 **Session hijacking** — Steal auth tokens
        - 🖼️ **Defacement** — Alter page content
        - 🎣 **Phishing** — Fake login popups
        """)
    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a1400,#201a00); border:1px solid #443300;
                    border-radius:14px; padding:22px; margin-top:10px;">
            <div style="font-family:'Orbitron',monospace; color:#ffcc00; font-size:0.95rem;
                        margin-bottom:16px; text-align:center;">💡 XSS ATTACK FLOW</div>
            <div style="font-family:'Share Tech Mono',monospace; color:#aa8833; font-size:0.82rem; line-height:2;">
                <div style="color:#ffdd44;">Step 1: Identify Reflection Point</div>
                <div style="color:#88771a; padding:4px 0 8px 12px;">URL params / form fields / headers</div>
                <div style="color:#ffdd44;">Step 2: Inject Test Payload</div>
                <div style="background:#0f0a00; border-radius:4px; padding:5px 10px; margin:4px 0 8px 0;
                            color:#66aa33; font-size:0.78rem;">&lt;script&gt;alert(1)&lt;/script&gt;</div>
                <div style="color:#ffdd44;">Step 3: Check Response</div>
                <div style="color:#88771a; padding:4px 0 8px 12px;">Is payload reflected unescaped?</div>
                <div style="color:#ffdd44;">Step 4: Craft Exploit</div>
                <div style="background:#0f0a00; border-radius:4px; padding:5px 10px; margin:4px 0;
                            color:#cc4422; font-size:0.78rem;">&lt;img src=x onerror=steal()&gt;</div>
            </div>
        </div>
        <div style="background:rgba(0,255,136,0.05); border:1px solid #004422;
                    border-radius:10px; padding:14px; margin-top:12px;">
            <div style="font-family:'Rajdhani',sans-serif; color:#00aa55; font-size:0.95rem;
                        font-weight:700; margin-bottom:6px;">✅ Prevention:</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#336644; font-size:0.88rem; line-height:1.7;">
                • <strong style="color:#00cc66;">Output Encoding</strong> — HTML escape all user data<br>
                • <strong style="color:#00cc66;">Content Security Policy (CSP)</strong> header<br>
                • Input validation & sanitization<br>
                • HTTPOnly cookies (prevent JS access)<br>
                • Use modern frameworks (React, Angular)
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div style="font-family:'Orbitron',monospace; color:#ffaa00; font-size:1.1rem;
            letter-spacing:1px; margin-bottom:12px;">
    🔍  SCAN FOR XSS VULNERABILITIES
</div>
""", unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    url = st.text_input("URL", placeholder="https://example.com/search?q=test", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("⚡  SCAN XSS", use_container_width=True)

if scan_btn:
    if not url:
        st.warning("⚠️  Please enter a URL to scan.")
    else:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        import time
        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#ffaa00; font-size:0.85rem;">⚡ Checking security headers...</div>', unsafe_allow_html=True)
        progress_bar.progress(20)
        time.sleep(0.3)

        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#ffaa00; font-size:0.85rem;">💉 Injecting XSS payloads into parameters...</div>', unsafe_allow_html=True)
        progress_bar.progress(50)

        res = check_xss(url)
        progress_bar.progress(90)

        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#ffaa00; font-size:0.85rem;">📊 Analyzing reflection points...</div>', unsafe_allow_html=True)
        time.sleep(0.2)
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)

        if res.get("error"):
            st.error(f"❌ {res['error']}")
        else:
            risk = res.get("risk_level","Low")
            risk_color = {"Critical":"#ff4444","High":"#ff8800","Medium":"#ffcc00","Low":"#00ff88"}.get(risk,"#00ff88")

            s1,s2,s3,s4 = st.columns(4)
            metrics = [
                ("XSS FOUND",   "YES ❌" if res["vulnerable"] else "NO ✅",
                 "#ff4444" if res["vulnerable"] else "#00ff88"),
                ("RISK LEVEL",  risk, risk_color),
                ("REFLECTED",   str(res.get("reflected_count",0)), "#ffcc00"),
                ("CSP HEADER",  "✅ SET" if res.get("csp_present") else "❌ MISSING",
                 "#00ff88" if res.get("csp_present") else "#ff4444"),
            ]
            for col, (label,val,color) in zip([s1,s2,s3,s4], metrics):
                with col:
                    st.markdown(f"""
                    <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                                border:1px solid {color}33; border-radius:12px; padding:18px 8px;">
                        <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                    letter-spacing:1px; margin-bottom:6px;">{label}</div>
                        <div style="font-family:'Orbitron',monospace; font-size:1.3rem; font-weight:700;
                                    color:{color};">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # CSP details
            tab1, tab2 = st.tabs(["📋  Findings", "🔐  Header Analysis"])

            with tab1:
                if res.get("vulnerable_params"):
                    st.markdown("**🎯 Vulnerable Parameters:**")
                    vp_html = "".join([
                        f'<span style="background:#1a1000;border:1px solid #ffcc00;color:#ffdd44;'
                        f'padding:4px 14px;border-radius:8px;margin:4px;display:inline-block;'
                        f'font-family:Share Tech Mono,monospace;font-size:0.88rem;">⚡ {p}</span>'
                        for p in res["vulnerable_params"]
                    ])
                    st.markdown(f'<div style="margin:8px 0 16px 0;">{vp_html}</div>', unsafe_allow_html=True)

                for f in res.get("findings", []):
                    ftype = f.get("type","info")
                    msg = f.get("message","")
                    payload = f.get("payload","")

                    if ftype == "reflected_xss":
                        st.markdown(f"""
                        <div style="background:#1a1400; border-left:4px solid #ffcc00;
                                    border-radius:0 8px 8px 0; padding:12px 16px; margin:6px 0;">
                            <div style="color:#ffdd44; font-family:'Share Tech Mono',monospace;
                                        font-size:0.88rem; font-weight:700;">⚡ REFLECTED XSS DETECTED</div>
                            <div style="color:#ccaa33; font-family:'Rajdhani',sans-serif;
                                        font-size:0.95rem; margin-top:4px;">{msg}</div>
                            {f'<div style="color:#886633; font-family:Share Tech Mono,monospace; font-size:0.78rem; margin-top:6px; background:#0d0a00; padding:6px 10px; border-radius:4px;">Payload: {payload}</div>' if payload else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    elif ftype == "warning":
                        st.warning(f"⚠️ {msg}")
                    else:
                        st.info(f"ℹ️ {msg}")

            with tab2:
                h_items = [
                    ("Content-Security-Policy", res.get("csp_header","Not Set"),
                     res.get("csp_present", False)),
                    ("X-XSS-Protection", res.get("x_xss_protection","Not Set"),
                     res.get("x_xss_protection","Not Set") not in ["Not Set","0"]),
                ]
                for h_name, h_val, h_present in h_items:
                    color = "#00ff88" if h_present else "#ff4444"
                    icon  = "✅" if h_present else "❌"
                    st.markdown(f"""
                    <div style="background:#080f1e; border:1px solid {color}33;
                                border-radius:8px; padding:12px 16px; margin:6px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-family:'Share Tech Mono',monospace; color:#4488aa; font-size:0.88rem;">{h_name}</span>
                            <span style="color:{color}; font-size:0.9rem;">{icon} {'Present' if h_present else 'Missing'}</span>
                        </div>
                        <div style="font-family:'Share Tech Mono',monospace; color:#336688;
                                    font-size:0.78rem; margin-top:5px; word-break:break-all;">
                            {h_val if h_val != "Not Set" else '<em style="color:#223344;">Header not found in response</em>'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
