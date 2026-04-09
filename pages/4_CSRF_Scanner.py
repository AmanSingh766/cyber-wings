import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.styles import get_cyber_theme, sidebar_logo
from utils.csrf_checker import check_csrf

st.set_page_config(page_title="CSRF Scanner — CyberWings", page_icon="🛡️", layout="wide")
st.markdown(get_cyber_theme(), unsafe_allow_html=True)
st.sidebar.markdown(sidebar_logo(), unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding:30px 0 5px 0;">
    <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                color:#ff8800; text-shadow:0 0 25px rgba(255,136,0,0.5); letter-spacing:2px;">
        🛡️ CSRF VULNERABILITY SCANNER
    </div>
    <div style="font-family:'Share Tech Mono',monospace; color:#aa5500; font-size:0.9rem; margin-top:6px;">
        Cross-Site Request Forgery — Form Token & Cookie Analysis
    </div>
    <div style="width:200px; height:2px;
                background:linear-gradient(90deg,transparent,#ff8800,transparent); margin:14px auto;"></div>
</div>
""", unsafe_allow_html=True)

with st.expander("📖  What is CSRF?  (Click to learn)", expanded=False):
    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.markdown("""
        ### 🛡️ Cross-Site Request Forgery (CSRF)

        **CSRF** tricks an authenticated user into unknowingly submitting a malicious request
        to a web application. The application processes it as legitimate because it comes with
        the user's valid session cookies.

        #### Classic CSRF Attack:
        1. User logs into `bank.com` (session cookie stored)
        2. User visits attacker's `evil.com`
        3. `evil.com` has hidden form: `POST /transfer?to=attacker&amount=5000`
        4. Browser auto-sends the bank cookie → **Money transferred!**

        #### CSRF vs XSS:
        | | CSRF | XSS |
        |--|------|-----|
        | **Trust** | Exploits site's trust in user | Exploits user's trust in site |
        | **Target** | State-changing actions | Data theft / script execution |
        | **Requires** | User must be authenticated | Script injection point |

        #### What CSRF Can Do:
        - 💸 Unauthorized fund transfers
        - 📧 Change email/password
        - 🗑️ Delete accounts/data
        - ⚙️ Change admin settings
        - 📤 Submit forms on behalf of user
        """)
    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a0800,#201200); border:1px solid #443300;
                    border-radius:14px; padding:22px; margin-top:10px;">
            <div style="font-family:'Orbitron',monospace; color:#ff8800; font-size:0.95rem;
                        margin-bottom:16px; text-align:center;">🔍 WHAT WE CHECK</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#aa6633; font-size:0.95rem; line-height:1.9;">
                <div style="margin-bottom:10px; border-left:2px solid #ff8800; padding-left:12px;">
                    <strong style="color:#ffaa44;">📝 Form Token Analysis</strong><br>
                    <span style="color:#775533; font-size:0.88rem;">Does each POST form have a CSRF token hidden field?</span>
                </div>
                <div style="margin-bottom:10px; border-left:2px solid #cc6600; padding-left:12px;">
                    <strong style="color:#ffaa44;">🍪 Cookie SameSite Attribute</strong><br>
                    <span style="color:#775533; font-size:0.88rem;">Are cookies set with SameSite=Strict/Lax?</span>
                </div>
                <div style="margin-bottom:10px; border-left:2px solid #aa4400; padding-left:12px;">
                    <strong style="color:#ffaa44;">🌐 CORS Misconfiguration</strong><br>
                    <span style="color:#775533; font-size:0.88rem;">Is ACAO set to wildcard (*)?</span>
                </div>
                <div style="border-left:2px solid #882200; padding-left:12px;">
                    <strong style="color:#ffaa44;">🔒 Secure + HttpOnly Flags</strong><br>
                    <span style="color:#775533; font-size:0.88rem;">Cookie security attribute analysis</span>
                </div>
            </div>
        </div>
        <div style="background:rgba(0,255,136,0.05); border:1px solid #004422;
                    border-radius:10px; padding:14px; margin-top:12px;">
            <div style="font-family:'Rajdhani',sans-serif; color:#00aa55; font-size:0.95rem;
                        font-weight:700; margin-bottom:6px;">✅ Prevention:</div>
            <div style="font-family:'Rajdhani',sans-serif; color:#336644; font-size:0.88rem; line-height:1.7;">
                • <strong style="color:#00cc66;">CSRF Tokens</strong> — unique per-request tokens<br>
                • <strong style="color:#00cc66;">SameSite=Strict</strong> cookie attribute<br>
                • Check <strong style="color:#00cc66;">Origin / Referer</strong> headers<br>
                • Double Submit Cookie pattern<br>
                • Custom request headers (AJAX)
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Orbitron',monospace; color:#ff8800; font-size:1.1rem;
            letter-spacing:1px; margin-bottom:12px;">
    🔍  SCAN FOR CSRF VULNERABILITIES
</div>
""", unsafe_allow_html=True)

col_input, col_btn = st.columns([4, 1])
with col_input:
    url = st.text_input("URL", placeholder="https://example.com/login", label_visibility="collapsed")
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("🛡️  SCAN CSRF", use_container_width=True)

if scan_btn:
    if not url:
        st.warning("⚠️  Please enter a URL to scan.")
    else:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        with st.spinner("🔍  Analyzing forms, cookies, and CORS headers..."):
            res = check_csrf(url)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<hr style="border-color:#0d2a4a;">', unsafe_allow_html=True)

        if res.get("error"):
            st.error(f"❌ {res['error']}")
        else:
            risk = res.get("risk_level","Low")
            risk_color = {"High":"#ff4444","Medium":"#ffcc00","Low":"#00ff88"}.get(risk,"#00ff88")

            s1,s2,s3,s4 = st.columns(4)
            metrics = [
                ("VULNERABLE",       "YES ❌" if res["vulnerable"] else "NO ✅",
                 "#ff4444" if res["vulnerable"] else "#00ff88"),
                ("RISK LEVEL",       risk, risk_color),
                ("FORMS FOUND",      str(res.get("forms_found",0)), "#00d4ff"),
                ("UNPROTECTED FORMS",str(res.get("forms_unprotected",0)),
                 "#ff4444" if res.get("forms_unprotected",0) > 0 else "#00ff88"),
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
            tab1, tab2, tab3 = st.tabs(["📝  Form Analysis", "🍪  Cookie Analysis", "🌐  CORS Analysis"])

            with tab1:
                forms = res.get("form_details", [])
                if not forms:
                    st.info("ℹ️ No HTML forms found on this page.")
                for form in forms:
                    protected = form.get("has_csrf_token", False)
                    border = "#00ff88" if protected else "#ff4444"
                    icon = "✅" if protected else "❌"
                    token_text = f"Token: <code>{form.get('token_field','N/A')}</code>" if protected else "No CSRF token found!"
                    st.markdown(f"""
                    <div style="background:#080f1e; border:1px solid {border}44;
                                border-left:4px solid {border}; border-radius:0 10px 10px 0;
                                padding:14px 18px; margin:8px 0;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-family:'Orbitron',monospace; color:{border}; font-size:0.9rem;">
                                {icon} Form #{form['form_id']} — METHOD: {form.get('method','GET')}
                            </span>
                            <span style="font-family:'Share Tech Mono',monospace; color:#336688; font-size:0.8rem;">
                                Action: {form.get('action','N/A')[:40]}
                            </span>
                        </div>
                        <div style="font-family:'Rajdhani',sans-serif; color:#4488aa; font-size:0.92rem; margin-top:8px;">
                            CSRF Protection: <strong style="color:{border};">{token_text}</strong>
                        </div>
                        {f'<div style="font-family:Rajdhani,sans-serif; color:#336655; font-size:0.85rem; margin-top:4px;">Sensitive Fields: {", ".join(form.get("sensitive_fields", []))}</div>' if form.get("sensitive_fields") else ''}
                    </div>
                    """, unsafe_allow_html=True)

            with tab2:
                cookies = res.get("cookie_analysis", [])
                if not cookies:
                    st.info("ℹ️ No cookies found in response.")
                for cookie in cookies:
                    risk_c = cookie.get("risk","Low")
                    c_color = {"High":"#ff4444","Medium":"#ffcc00","Low":"#00ff88"}.get(risk_c,"#00ff88")
                    st.markdown(f"""
                    <div style="background:#080f1e; border:1px solid {c_color}33;
                                border-radius:10px; padding:12px 16px; margin:6px 0;">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="font-family:'Share Tech Mono',monospace; color:#55aacc;">{cookie['name']}</span>
                            <span style="background:{c_color}20; color:{c_color}; border:1px solid {c_color}55;
                                         padding:2px 10px; border-radius:8px; font-size:0.75rem;
                                         font-family:Share Tech Mono,monospace;">{risk_c} RISK</span>
                        </div>
                        <div style="display:flex; gap:12px; margin-top:8px; flex-wrap:wrap;">
                            <span style="font-family:Share Tech Mono,monospace; font-size:0.78rem;
                                         color:{'#00ff88' if cookie.get('secure') else '#ff4444'};">
                                {'✅' if cookie.get('secure') else '❌'} Secure</span>
                            <span style="font-family:Share Tech Mono,monospace; font-size:0.78rem;
                                         color:{'#00ff88' if cookie.get('httponly') else '#ffcc00'};">
                                {'✅' if cookie.get('httponly') else '⚠️'} HttpOnly</span>
                            <span style="font-family:Share Tech Mono,monospace; font-size:0.78rem;
                                         color:{'#00ff88' if cookie.get('samesite') not in ['Not Set','None'] else '#ff4444'};">
                                🍪 SameSite={cookie.get('samesite','Not Set')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            with tab3:
                cors = res.get("cors_analysis", {})
                acao = cors.get("allow_origin","Not Set")
                acac = cors.get("allow_credentials","Not Set")
                acao_risky = acao == "*"
                st.markdown(f"""
                <div style="background:#080f1e; border:1px solid {'#ff444433' if acao_risky else '#0d2a4a'};
                            border-radius:10px; padding:16px 20px;">
                    <div style="font-family:'Share Tech Mono',monospace; font-size:0.9rem; line-height:2.5;">
                        <div>
                            <span style="color:#2255aa;">Access-Control-Allow-Origin :</span>
                            <span style="color:{'#ff4444' if acao_risky else '#00ff88'};"> {acao}
                                {'⚠️ WILDCARD — High Risk!' if acao_risky else ''}</span>
                        </div>
                        <div>
                            <span style="color:#2255aa;">Access-Control-Allow-Credentials :</span>
                            <span style="color:#88ccee;"> {acac}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                for f in res.get("findings", []):
                    ftype = f.get("type","info")
                    msg = f.get("message","")
                    if "cors" in ftype:
                        st.error(f"🔴 {msg}")
                    elif ftype == "info":
                        st.info(f"ℹ️ {msg}")
