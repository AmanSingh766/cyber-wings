import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, sidebar_logo
from utils.sql_checker import check_sql_injection

st.set_page_config(page_title="SQL Injection — CyberWings", page_icon="💉", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#ff4444; text-shadow:0 0 25px rgba(255,68,68,0.5); letter-spacing:2px;">
        💉 SQL INJECTION SCANNER
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#aa3333; font-size:0.9rem; margin-top:6px;">
        Detect Error-Based & Time-Based Blind SQLi Vulnerabilities
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#ff4444,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

# ─── ABOUT SQL INJECTION ─────────────────────────────────────────────────────
with st.expander("📖  What is SQL Injection?  (Click to learn)", expanded=False):
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.markdown("""
        ### 💉 SQL Injection — #1 Web Attack

        **SQL Injection (SQLi)** is a code injection technique that exploits vulnerabilities
        in an application's database query handling. It is consistently ranked **#1 in the
        OWASP Top 10** web application security risks.

        #### How It Works:
        An attacker injects **malicious SQL code** into input fields that are concatenated
        directly into database queries without proper sanitization.

        **Vulnerable Code (PHP example):**
        ```sql
        SELECT * FROM users WHERE id = '$_GET[id]'
        ```
        **Attack Input:** `1' OR '1'='1`

        **Resulting Query (always TRUE → dumps all users!):**
        ```sql
        SELECT * FROM users WHERE id = '1' OR '1'='1'
        ```

        #### Types of SQL Injection:
        | Type | Description |
        |------|-------------|
        | **Error-Based** | SQL errors leak database info |
        | **Union-Based** | UNION to extract data from other tables |
        | **Blind Boolean** | True/false conditions reveal data bit by bit |
        | **Time-Based Blind** | SLEEP() delays used to infer data |
        | **Out-of-Band** | DNS/HTTP channels used for data extraction |
        """)
    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a0000,#200a0a); border:1px solid #441111;
                    border-radius:14px; padding:22px; margin-top:10px;">
            <div style="font-family:'Orbitron',monospace; color:#ff4444; font-size:0.95rem;
                        margin-bottom:16px; text-align:center;">💥 IMPACT OF SQLi</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#cc6666; font-size:0.95rem; line-height:1.9;">
                <div style="border-left:2px solid #ff4444; padding-left:12px; margin-bottom:8px;">
                    🔓 <strong style="color:#ff6666;">Authentication Bypass</strong><br>
                    <span style="color:#884444;">Login as any user without password</span>
                </div>
                <div style="border-left:2px solid #cc3333; padding-left:12px; margin-bottom:8px;">
                    📦 <strong style="color:#ff6666;">Data Exfiltration</strong><br>
                    <span style="color:#884444;">Dump entire database tables</span>
                </div>
                <div style="border-left:2px solid #aa2222; padding-left:12px; margin-bottom:8px;">
                    ✏️ <strong style="color:#ff6666;">Data Manipulation</strong><br>
                    <span style="color:#884444;">INSERT, UPDATE, DELETE records</span>
                </div>
                <div style="border-left:2px solid #881111; padding-left:12px;">
                    🖥️ <strong style="color:#ff6666;">OS Command Execution</strong><br>
                    <span style="color:#884444;">Full server compromise via xp_cmdshell</span>
                </div>
            </div>
        </div>
        <div style="background:rgba(0,255,136,0.05); border:1px solid #004422;
                    border-radius:10px; padding:14px; margin-top:12px;">
            <div style="font-family:'Rajdhani',sans-serif; color:#00aa55; font-size:0.95rem;
                        font-weight:700; margin-bottom:6px;">✅ Prevention:</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#336644; font-size:0.88rem; line-height:1.7;">
                • Use <strong style="color:#00cc66;">Parameterized Queries</strong> / Prepared Statements<br>
                • Input validation & whitelisting<br>
                • Least privilege DB accounts<br>
                • Web Application Firewall (WAF)<br>
                • ORM frameworks (SQLAlchemy, Hibernate)
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── SCANNER ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Orbitron',monospace; color:#ff6644; font-size:1.1rem;
            letter-spacing:1px; margin-bottom:12px;">
    🔍  SCAN FOR SQL INJECTION
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(255,100,0,0.05); border:1px solid #443300;
            border-radius:8px; padding:10px 15px; margin-bottom:14px;
            font-family:'Share Tech Mono',monospace; color:#886644; font-size:0.82rem;">
    ℹ️  For best results, provide a URL with query parameters. Example: https://example.com/page?id=1&cat=2
</div>
""", unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    url = st.text_input("URL", placeholder="https://example.com/page?id=1", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("💉  SCAN SQLi", use_container_width=True)

if scan_btn:
    if not url:
        st.warning("⚠️  Please enter a URL to scan.")
    else:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#0088ff; font-size:0.85rem;">🔍 Initializing SQL injection scanner...</div>', unsafe_allow_html=True)
        progress_bar.progress(15)

        import time
        time.sleep(0.3)
        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#0088ff; font-size:0.85rem;">💉 Injecting payloads into parameters...</div>', unsafe_allow_html=True)
        progress_bar.progress(40)

        res = check_sql_injection(url)
        progress_bar.progress(85)

        status_text.markdown('<div style="font-family:Share Tech Mono,monospace; color:#0088ff; font-size:0.85rem;">📊 Analyzing responses for SQL errors...</div>', unsafe_allow_html=True)
        time.sleep(0.3)
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)

        if res.get("error"):
            st.error(f"❌ Scanner Error: {res['error']}")
        else:
            risk = res.get("risk_level", "Low")
            risk_color = {"Critical":"#ff4444","High":"#ff8800","Medium":"#ffcc00","Low":"#00ff88"}.get(risk,"#00ff88")

            # Summary row
            s1, s2, s3, s4 = st.columns(4)
            metrics = [
                ("VULNERABLE", "YES ❌" if res["vulnerable"] else "NO ✅",
                 "#ff4444" if res["vulnerable"] else "#00ff88"),
                ("RISK LEVEL", risk, risk_color),
                ("PARAMS TESTED", str(len(res.get("parameters_tested", []))), "#00d4ff"),
                ("TOTAL TESTS", str(res.get("total_tests", 0)), "#00aaff"),
            ]
            for col, (label, val, color) in zip([s1,s2,s3,s4], metrics):
                with col:
                    st.markdown(f"""
                    <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                                border:1px solid {color}33; border-radius:12px; padding:18px 8px;">
                        <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                    letter-spacing:1px; margin-bottom:6px;">{label}</div>
                        <div style="font-family:'Orbitron',monospace; font-size:1.4rem; font-weight:700;
                                    color:{color};">{val}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Vulnerable params
            if res.get("vulnerable_params"):
                st.markdown("**🎯 Vulnerable Parameters:**")
                vp_html = "".join([
                    f'<span style="background:#1a0000;border:1px solid #ff4444;color:#ff6666;'
                    f'padding:4px 14px;border-radius:8px;margin:4px;display:inline-block;'
                    f'font-family:Share Tech Mono,monospace;font-size:0.88rem;">⚠️ {p}</span>'
                    for p in res["vulnerable_params"]
                ])
                st.markdown(f'<div style="margin:8px 0 16px 0;">{vp_html}</div>', unsafe_allow_html=True)

            # Findings
            if res.get("findings"):
                st.markdown("**📋 Detailed Findings:**")
                for f in res["findings"]:
                    ftype = f.get("type","info")
                    msg = f.get("message","")
                    evidence = f.get("evidence","")
                    payload = f.get("payload","")

                    if ftype == "error_based":
                        st.markdown(f"""
                        <div style="background:#1a0305; border-left:4px solid #ff4444;
                                    border-radius:0 8px 8px 0; padding:12px 16px; margin:6px 0;">
                            <div style="color:#ff6666; font-family:'Share Tech Mono',monospace;
                                        font-size:0.88rem; font-weight:700;">🔴 ERROR-BASED SQLi DETECTED</div>
                            <div style="color:#cc4444; font-family:'Rajdhani',sans-serif;
                                        font-size:0.95rem; margin-top:4px;">{msg}</div>
                            {f'<div style="color:#884444; font-family:Share Tech Mono,monospace; font-size:0.8rem; margin-top:6px; background:#0d0000; padding:6px 10px; border-radius:4px;">Payload: {payload}</div>' if payload else ''}
                            {f'<div style="color:#663333; font-family:Share Tech Mono,monospace; font-size:0.78rem; margin-top:4px;">Evidence: {evidence}</div>' if evidence else ''}
                        </div>
                        """, unsafe_allow_html=True)
                    elif ftype == "time_based":
                        st.markdown(f"""
                        <div style="background:#1a0a00; border-left:4px solid #ff8800;
                                    border-radius:0 8px 8px 0; padding:12px 16px; margin:6px 0;">
                            <div style="color:#ffaa44; font-family:'Share Tech Mono',monospace;
                                        font-size:0.88rem; font-weight:700;">🟠 TIME-BASED SQLi POSSIBLE</div>
                            <div style="color:#cc8844; font-family:'Rajdhani',sans-serif;
                                        font-size:0.95rem; margin-top:4px;">{msg}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif "info" in ftype:
                        st.info(f"ℹ️ {msg}")

            # Params tested
            if res.get("parameters_tested"):
                with st.expander("🔬 Parameters Tested"):
                    for p in res["parameters_tested"]:
                        st.markdown(f"• `{p}`")
