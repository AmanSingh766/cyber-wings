import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, sidebar_logo
from utils.advanced_checker import (
    check_security_headers, check_sensitive_files,
    check_open_redirect, check_ports
)

st.set_page_config(page_title="Advanced Scanner — CyberWings", page_icon="🔍", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#aa44ff; text-shadow:0 0 25px rgba(170,68,255,0.5); letter-spacing:2px;">
        🔍 ADVANCED VULNERABILITY SCANNER
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#6622aa; font-size:0.9rem; margin-top:6px;">
        Security Headers • Sensitive Files • Open Redirect • Port Intelligence
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#aa44ff,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Scan options
st.markdown("""
<div style="font-family:'Orbitron',monospace; color:#8833cc; font-size:1.1rem;
            letter-spacing:1px; margin-bottom:12px;">
    ⚙️  CONFIGURE YOUR SCAN
</div>
""", unsafe_allow_html=True)

col_url, col_btn = st.columns([4, 1])
with col_url:
    url = st.text_input("Target URL", placeholder="https://example.com", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("🔍  LAUNCH SCAN", use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    do_headers = st.checkbox("🔐 Security Headers", value=True)
with c2:
    do_files = st.checkbox("📂 Sensitive Files", value=True)
with c3:
    do_redirect = st.checkbox("🔄 Open Redirect", value=True)
with c4:
    do_ports = st.checkbox("🌐 Port Scan", value=True)

if scan_btn:
    if not url:
        st.warning("⚠️  Please enter a URL.")
    else:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; color:#8833cc; font-size:1.1rem;
                    letter-spacing:1px; margin:10px 0 18px 0;">
            📊  ADVANCED SCAN RESULTS
        </div>
        """, unsafe_allow_html=True)

        # ── SECURITY HEADERS ────────────────────────────────────────────────
        if do_headers:
            with st.spinner("🔐 Auditing security headers..."):
                h_res = check_security_headers(url)

            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700;
                        color:#00aaff; margin:16px 0 8px 0;">
                🔐 SECURITY HEADERS AUDIT
            </div>
            """, unsafe_allow_html=True)

            if h_res.get("error"):
                st.error(f"❌ {h_res['error']}")
            else:
                grade = h_res.get("grade","F")
                score = h_res.get("score",0)
                grade_colors = {"A+":"#00ff88","A":"#00cc66","B":"#88ff00","C":"#ffcc00","D":"#ff8800","F":"#ff4444"}
                gc = grade_colors.get(grade,"#ff4444")

                hc1, hc2 = st.columns([1,3])
                with hc1:
                    st.markdown(f"""
                    <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                                border:2px solid {gc}; border-radius:14px; padding:20px;">
                        <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace;">HEADER GRADE</div>
                        <div style="font-family:'Orbitron',monospace; font-size:3rem; font-weight:900;
                                    color:{gc}; text-shadow:0 0 15px {gc}80;">{grade}</div>
                        <div style="font-family:'Rajdhani',sans-serif; color:{gc}; font-size:1rem;">{score}/100</div>
                    </div>
                    """, unsafe_allow_html=True)

                with hc2:
                    st.markdown("**✅ Present Headers:**")
                    for h, meta in h_res.get("present",{}).items():
                        risk_c = {"High":"#00ff88","Medium":"#88ff00","Low":"#00aaff"}.get(meta["risk"],"#00aaff")
                        st.markdown(f"""
                        <div style="background:#071510; border:1px solid #00ff8830; border-radius:6px;
                                    padding:8px 14px; margin:3px 0; display:flex; justify-content:space-between;">
                            <span style="font-family:'Share Tech Mono',monospace; color:#00cc66; font-size:0.82rem;">✅ {h}</span>
                            <span style="font-family:'Rajdhani',sans-serif; color:#336644; font-size:0.82rem;">{meta['desc']}</span>
                        </div>
                        """, unsafe_allow_html=True)

                    if h_res.get("missing"):
                        st.markdown("**❌ Missing Headers:**")
                        for h, meta in h_res["missing"].items():
                            risk_c = {"High":"#ff4444","Medium":"#ffcc00","Low":"#ff8800"}.get(meta["risk"],"#ffcc00")
                            st.markdown(f"""
                            <div style="background:#150500; border:1px solid {risk_c}33; border-radius:6px;
                                        padding:8px 14px; margin:3px 0; display:flex; justify-content:space-between;">
                                <span style="font-family:'Share Tech Mono',monospace; color:{risk_c}; font-size:0.82rem;">❌ {h}</span>
                                <span style="font-family:'Rajdhani',sans-serif; color:#664422; font-size:0.82rem;">[{meta['risk']}] {meta['desc']}</span>
                            </div>
                            """, unsafe_allow_html=True)

                # Info headers (X-Powered-By, Server)
                info_h = h_res.get("info_headers",{})
                if info_h:
                    with st.expander("ℹ️ Info / Disclosure Headers"):
                        for h, meta in info_h.items():
                            if meta.get("present"):
                                st.warning(f"⚠️ **{h}**: `{meta['value']}` — {meta['desc']}")
                            else:
                                st.success(f"✅ **{h}**: Not exposed — {meta['desc']}")

            st.markdown("<br>", unsafe_allow_html=True)

        # ── SENSITIVE FILES ──────────────────────────────────────────────────
        if do_files:
            with st.spinner("📂 Probing for sensitive files & directories..."):
                f_res = check_sensitive_files(url)

            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700;
                        color:#ff8800; margin:16px 0 8px 0;">
                📂 SENSITIVE FILE EXPOSURE
            </div>
            """, unsafe_allow_html=True)

            found = f_res.get("found", [])
            critical_count = f_res.get("critical_count", 0)

            fc1, fc2, fc3 = st.columns(3)
            with fc1:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid {'#ff444433' if found else '#00ff8833'}; border-radius:12px; padding:16px 8px;">
                    <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace; margin-bottom:6px;">FILES FOUND</div>
                    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:700;
                                color:{'#ff4444' if found else '#00ff88'};">{len(found)}</div>
                </div>""", unsafe_allow_html=True)
            with fc2:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid {'#ff000033' if critical_count else '#0d2a4a'}; border-radius:12px; padding:16px 8px;">
                    <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace; margin-bottom:6px;">CRITICAL FILES</div>
                    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:700;
                                color:{'#ff0000' if critical_count else '#00ff88'};">{critical_count}</div>
                </div>""", unsafe_allow_html=True)
            with fc3:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid #0d2a4a; border-radius:12px; padding:16px 8px;">
                    <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace; margin-bottom:6px;">FILES CHECKED</div>
                    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:700; color:#00d4ff;">
                        {len(found) + len(f_res.get('not_found',[]))}</div>
                </div>""", unsafe_allow_html=True)

            if found:
                st.markdown("<br>**⚠️ Exposed Files:**")
                for fi in found:
                    is_crit = fi.get("critical", False)
                    status_c = "#ff0000" if is_crit else "#ff8800" if fi.get("status") == 200 else "#ffcc00"
                    st.markdown(f"""
                    <div style="background:{'#150000' if is_crit else '#100800'}; border:1px solid {status_c}44;
                                border-left:4px solid {status_c}; border-radius:0 8px 8px 0;
                                padding:10px 16px; margin:5px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <code style="color:{status_c}; font-size:0.88rem;">/{fi['path']}</code>
                            <span style="font-family:Share Tech Mono,monospace; font-size:0.75rem;
                                         color:{status_c};">HTTP {fi['status']} {'🔴 CRITICAL' if is_crit else ''}</span>
                        </div>
                        {f'<div style="font-family:Share Tech Mono,monospace; color:#664422; font-size:0.75rem; margin-top:5px; word-break:break-all;">Preview: {fi.get("content_preview","")[:80]}</div>' if fi.get("content_preview") and fi.get("status") == 200 else ''}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No sensitive files or directories exposed.")

            st.markdown("<br>", unsafe_allow_html=True)

        # ── OPEN REDIRECT ────────────────────────────────────────────────────
        if do_redirect:
            with st.spinner("🔄 Testing open redirect parameters..."):
                r_res = check_open_redirect(url)

            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700;
                        color:#00d4ff; margin:16px 0 8px 0;">
                🔄 OPEN REDIRECT TEST
            </div>
            """, unsafe_allow_html=True)

            rc1, rc2 = st.columns(2)
            with rc1:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid {'#ff444433' if r_res.get('vulnerable') else '#00ff8833'}; border-radius:12px; padding:16px 8px;">
                    <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace; margin-bottom:6px;">VULNERABLE</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700;
                                color:{'#ff4444' if r_res.get('vulnerable') else '#00ff88'};">
                        {'YES ❌' if r_res.get('vulnerable') else 'NO ✅'}</div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid #0d2a4a; border-radius:12px; padding:16px 8px;">
                    <div style="font-size:0.75rem; color:#4488aa; font-family:'Share Tech Mono',monospace; margin-bottom:6px;">PARAMS TESTED</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700; color:#00d4ff;">
                        {r_res.get('tests_done',0)}</div>
                </div>""", unsafe_allow_html=True)

            for finding in r_res.get("findings",[]):
                if finding.get("type") == "open_redirect":
                    st.error(f"🔴 {finding['message']}")
                else:
                    st.success(f"✅ {finding['message']}")

            st.markdown("<br>", unsafe_allow_html=True)

        # ── PORT SCAN ────────────────────────────────────────────────────────
        if do_ports:
            with st.spinner("🌐 Scanning common ports..."):
                p_res = check_ports(url)

            st.markdown("""
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700;
                        color:#aa44ff; margin:16px 0 8px 0;">
                🌐 PORT INTELLIGENCE
            </div>
            """, unsafe_allow_html=True)

            if p_res.get("error"):
                st.error(f"❌ {p_res['error']}")
            else:
                st.markdown(f"**🖥️ Host:** `{p_res.get('host','N/A')}`")

                open_ports = p_res.get("open", [])
                DANGER_PORTS = {21,23,3389,445}
                WARN_PORTS   = {22,3306,5432,6379,27017}

                if open_ports:
                    st.markdown(f"**🔓 Open Ports ({len(open_ports)}):**")
                    pcols = st.columns(min(len(open_ports), 4))
                    for i, port_info in enumerate(open_ports):
                        p = port_info["port"]
                        s = port_info["service"]
                        if p in DANGER_PORTS:
                            pc = "#ff4444"; label = "DANGER"
                        elif p in WARN_PORTS:
                            pc = "#ffcc00"; label = "WARNING"
                        else:
                            pc = "#00ff88"; label = "OPEN"
                        with pcols[i % 4]:
                            st.markdown(f"""
                            <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                                        border:1px solid {pc}44; border-radius:10px; padding:14px 8px; margin:4px 0;">
                                <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:{pc}; font-weight:700;">{p}</div>
                                <div style="font-family:'Share Tech Mono',monospace; color:#336688; font-size:0.8rem;">{s}</div>
                                <div style="background:{pc}20; color:{pc}; border:1px solid {pc}55;
                                             padding:2px 8px; border-radius:8px; font-size:0.7rem;
                                             font-family:Share Tech Mono,monospace; margin-top:6px; display:inline-block;">{label}</div>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.success("✅ No open ports detected on common ports.")

                with st.expander(f"📋 All Ports Scanned ({len(p_res.get('closed',[]))} closed)"):
                    for cp in p_res.get("closed", []):
                        st.markdown(f"• Port `{cp['port']}` ({cp['service']}) — Closed/Filtered")
