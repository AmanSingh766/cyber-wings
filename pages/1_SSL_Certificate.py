import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, cyber_card, status_badge, sidebar_logo
from utils.ssl_checker import check_ssl

st.set_page_config(page_title="SSL Analyzer — CyberWings", page_icon="🔒", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#00d4ff; text-shadow:0 0 25px rgba(0,212,255,0.6); letter-spacing:2px;">
        🔒 SSL CERTIFICATE ANALYZER
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#0077aa; font-size:0.9rem; margin-top:6px;">
        Inspect, Validate & Grade SSL/TLS Certificates
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#00d4ff,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

# ─── ABOUT SSL SECTION ───────────────────────────────────────────────────────
with st.expander("📖  What is an SSL Certificate?  (Click to learn)", expanded=False):
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.markdown("""
        ### 🔐 SSL / TLS — The Backbone of Web Security

        **SSL (Secure Sockets Layer)** and its modern successor **TLS (Transport Layer Security)**
        are cryptographic protocols that establish an encrypted connection between a web server
        and a client (browser).

        #### How It Works:
        1. **Handshake** — Server presents its certificate to the client
        2. **Verification** — Client verifies the certificate against trusted CAs
        3. **Key Exchange** — Symmetric session keys are exchanged securely
        4. **Encrypted Communication** — All data is now encrypted

        #### What SSL Certificates Protect:
        - 🔏 **Data in transit** — Passwords, credit cards, personal info
        - 🌐 **Identity** — Confirms you're talking to the real server
        - ✅ **Integrity** — Data cannot be tampered in transit

        #### Certificate Types:
        | Type | Description |
        |------|-------------|
        | **DV** | Domain Validated — basic, fast |
        | **OV** | Organization Validated — business verified |
        | **EV** | Extended Validation — highest trust level |
        | **Wildcard** | Covers all subdomains (*.example.com) |
        """)
    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#070e1d,#0b1a30); border:1px solid #0d3a6a;
                    border-radius:14px; padding:22px; margin-top:10px;">
            <div style="font-family:'Orbitron',monospace; color:#00d4ff; font-size:1rem;
                        margin-bottom:16px; text-align:center;">🔒 SSL LIFECYCLE</div>
            <div style="font-family:'Share Tech Mono',monospace; color:#4499cc; font-size:0.85rem;
                        line-height:2.2;">
                <div style="border-left:2px solid #00d4ff; padding-left:12px; margin-bottom:8px;">
                    ➤ Certificate Issued by CA<br>
                    <span style="color:#336688; font-size:0.75rem;">DigiCert, Let's Encrypt, Comodo...</span>
                </div>
                <div style="border-left:2px solid #0077aa; padding-left:12px; margin-bottom:8px;">
                    ➤ Domain Verification<br>
                    <span style="color:#336688; font-size:0.75rem;">DNS record / File upload / Email</span>
                </div>
                <div style="border-left:2px solid #004466; padding-left:12px; margin-bottom:8px;">
                    ➤ Installed on Server<br>
                    <span style="color:#336688; font-size:0.75rem;">Apache, Nginx, IIS, Cloudflare...</span>
                </div>
                <div style="border-left:2px solid #002244; padding-left:12px; margin-bottom:8px;">
                    ➤ Browser Validates<br>
                    <span style="color:#336688; font-size:0.75rem;">Certificate chain checked</span>
                </div>
                <div style="border-left:2px solid #001122; padding-left:12px;">
                    ➤ Expires (renew!) ⚠️<br>
                    <span style="color:#336688; font-size:0.75rem;">Typically 90 days – 1 year</span>
                </div>
            </div>
        </div>

        <div style="background:rgba(255,100,0,0.06); border:1px solid #442200;
                    border-radius:10px; padding:14px; margin-top:12px;">
            <div style="font-family:'Rajdhani',sans-serif; color:#ff8844; font-size:0.95rem;
                        font-weight:700; margin-bottom:6px;">⚠️ Risks of Missing SSL:</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#886644; font-size:0.88rem; line-height:1.7;">
                • Man-in-the-Middle (MitM) attacks<br>
                • Credential & session theft<br>
                • SEO penalization by Google<br>
                • Browser security warnings<br>
                • Data integrity compromise
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── SCANNER UI ──────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Orbitron',monospace; color:#00aaff; font-size:1.1rem;
            letter-spacing:1px; margin-bottom:12px;">
    🔍  ANALYZE A WEBSITE
</div>
""", unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("🔒  SCAN SSL", use_container_width=True)

# ─── SCAN RESULTS ────────────────────────────────────────────────────────────
if scan_btn:
    if not url:
        st.warning("⚠️  Please enter a URL to analyze.")
    else:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        with st.spinner("🔍  Connecting and analyzing SSL certificate..."):
            res = check_ssl(url)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Orbitron',monospace; color:#00aaff; font-size:1.1rem;
                    letter-spacing:1px; margin:10px 0 18px 0;">
            📊  SCAN RESULTS
        </div>
        """, unsafe_allow_html=True)

        if res.get("error") and not res.get("cert"):
            st.error(f"❌  {res['error']}")
        else:
            cert = res.get("cert", {})

            # Grade + Status row
            grade_colors = {
                "A+": "#00ff88", "A": "#00cc66", "B": "#88ff00",
                "C": "#ffcc00", "D": "#ff8800", "F": "#ff4444"
            }
            grade = res.get("grade", "F")
            grade_color = grade_colors.get(grade, "#ff4444")

            g1, g2, g3, g4 = st.columns(4)
            with g1:
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:2px solid {grade_color}; border-radius:14px; padding:20px 10px;">
                    <div style="font-size:0.8rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                letter-spacing:1px; margin-bottom:4px;">SSL GRADE</div>
                    <div style="font-family:'Orbitron',monospace; font-size:3.5rem; font-weight:900;
                                color:{grade_color}; text-shadow:0 0 20px {grade_color}80;">{grade}</div>
                </div>
                """, unsafe_allow_html=True)

            with g2:
                ssl_status = "✅ Active" if res.get("has_ssl") else "❌ No SSL"
                ssl_color = "#00ff88" if res.get("has_ssl") else "#ff4444"
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid {ssl_color}44; border-radius:14px; padding:20px 10px;">
                    <div style="font-size:0.8rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                letter-spacing:1px; margin-bottom:8px;">STATUS</div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:1.4rem; font-weight:700;
                                color:{ssl_color};">{ssl_status}</div>
                </div>
                """, unsafe_allow_html=True)

            with g3:
                days = cert.get("days_left", "N/A")
                days_color = "#00ff88" if isinstance(days, int) and days > 30 else "#ffcc00" if isinstance(days, int) and days > 7 else "#ff4444"
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid #0d2a4a; border-radius:14px; padding:20px 10px;">
                    <div style="font-size:0.8rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                letter-spacing:1px; margin-bottom:8px;">DAYS LEFT</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.8rem; font-weight:700;
                                color:{days_color};">{days}</div>
                </div>
                """, unsafe_allow_html=True)

            with g4:
                tls = cert.get("tls_version", "N/A")
                tls_color = "#00ff88" if "1.3" in str(tls) else "#00aaff" if "1.2" in str(tls) else "#ff4444"
                st.markdown(f"""
                <div style="text-align:center; background:linear-gradient(135deg,#070e1d,#0c1629);
                            border:1px solid #0d2a4a; border-radius:14px; padding:20px 10px;">
                    <div style="font-size:0.8rem; color:#4488aa; font-family:'Share Tech Mono',monospace;
                                letter-spacing:1px; margin-bottom:8px;">TLS VERSION</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.5rem; font-weight:700;
                                color:{tls_color};">{tls}</div>
                </div>
                """, unsafe_allow_html=True)

            if cert:
                st.markdown("<br>", unsafe_allow_html=True)
                tab1, tab2, tab3 = st.tabs(["📋  Certificate Details", "🔐  Cipher & Protocol", "⚠️  Issues & Recommendations"])

                with tab1:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"""
                        <div style="font-family:'Share Tech Mono',monospace; font-size:0.9rem; line-height:2.2; color:#4499cc;">
                            <div><span style="color:#2255aa;">Common Name :</span>
                                 <span style="color:#88ccee;">{cert.get('common_name','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Organization :</span>
                                 <span style="color:#88ccee;">{cert.get('organization','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Issuer (CN)  :</span>
                                 <span style="color:#88ccee;">{cert.get('issuer_cn','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Issuer (Org) :</span>
                                 <span style="color:#88ccee;">{cert.get('issuer_org','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Serial No    :</span>
                                 <span style="color:#558899; font-size:0.78rem;">{cert.get('serial','N/A')[:32]}...</span></div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown(f"""
                        <div style="font-family:'Share Tech Mono',monospace; font-size:0.9rem; line-height:2.2; color:#4499cc;">
                            <div><span style="color:#2255aa;">Valid From   :</span>
                                 <span style="color:#88ccee;">{cert.get('not_before','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Expires On   :</span>
                                 <span style="color:#88ccee;">{cert.get('not_after','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Days Left    :</span>
                                 <span style="color:#88ccee;">{cert.get('days_left','N/A')}</span></div>
                            <div><span style="color:#2255aa;">Expired?     :</span>
                                 <span style="color:{'#ff4444' if cert.get('is_expired') else '#00ff88'};">{'YES ❌' if cert.get('is_expired') else 'NO ✅'}</span></div>
                        </div>
                        """, unsafe_allow_html=True)

                    if cert.get("sans"):
                        st.markdown("<br>**🌐 Subject Alternative Names (SANs):**", unsafe_allow_html=False)
                        sans_html = "".join([
                            f'<span style="background:#051525;border:1px solid #0d3a5a;color:#55aacc;'
                            f'padding:3px 10px;border-radius:6px;margin:3px;display:inline-block;'
                            f'font-family:Share Tech Mono,monospace;font-size:0.82rem;">{s}</span>'
                            for s in cert["sans"]
                        ])
                        st.markdown(f'<div style="margin-top:6px;">{sans_html}</div>', unsafe_allow_html=True)

                with tab2:
                    st.markdown(f"""
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.95rem; line-height:2.5; color:#4499cc;">
                        <div><span style="color:#2255aa;">Cipher Suite  :</span>
                             <span style="color:#88ccee;">{cert.get('cipher_name','N/A')}</span></div>
                        <div><span style="color:#2255aa;">Key Strength   :</span>
                             <span style="color:{'#00ff88' if (cert.get('cipher_bits') or 0) >= 128 else '#ff4444'};">
                             {cert.get('cipher_bits','N/A')} bits
                             {'✅' if (cert.get('cipher_bits') or 0) >= 128 else '❌ Weak'}</span></div>
                        <div><span style="color:#2255aa;">TLS Version    :</span>
                             <span style="color:{'#00ff88' if '1.3' in str(cert.get('tls_version','')) else '#00aaff'};">
                             {cert.get('tls_version','N/A')}
                             {'✅ Excellent' if '1.3' in str(cert.get('tls_version','')) else '🔵 Acceptable' if '1.2' in str(cert.get('tls_version','')) else '❌ Outdated'}</span></div>
                        <div><span style="color:#2255aa;">Hostname       :</span>
                             <span style="color:#88ccee;">{cert.get('hostname','N/A')}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                with tab3:
                    issues = res.get("issues", [])
                    recs = res.get("recommendations", [])

                    if issues:
                        st.markdown("**⚠️ Issues Found:**")
                        for issue in issues:
                            if "No critical" in issue:
                                st.success(f"✅ {issue}")
                            elif "EXPIRED" in issue or "Critical" in issue:
                                st.error(f"🔴 {issue}")
                            else:
                                st.warning(f"🟡 {issue}")

                    if recs:
                        st.markdown("<br>**💡 Recommendations:**")
                        for rec in recs:
                            st.info(f"➤ {rec}")

            if res.get("error"):
                st.error(f"⚠️ Note: {res['error']}")
