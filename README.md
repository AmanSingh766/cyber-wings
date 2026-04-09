# 🛡️ CyberWings — Web Vulnerability Scanner

A professional multi-page cybersecurity dashboard built with **Python + Streamlit**.

## 📁 Folder Structure

```
cyber_wings/
├── app.py                      ← Main Dashboard (Home Page)
├── requirements.txt
├── README.md
├── pages/
│   ├── 1_🔒_SSL_Certificate.py    ← SSL Analyzer
│   ├── 2_💉_SQL_Injection.py      ← SQLi Scanner
│   ├── 3_⚡_XSS_Scanner.py        ← XSS Scanner
│   ├── 4_🛡️_CSRF_Scanner.py       ← CSRF Scanner
│   ├── 5_🔍_Advanced_Scanner.py   ← Advanced (Headers/Files/Redirect/Ports)
│   └── 6_👥_About_Us.py           ← About The Team
└── utils/
    ├── __init__.py
    ├── styles.py               ← Cyber Blue CSS theme
    ├── ssl_checker.py          ← SSL logic
    ├── sql_checker.py          ← SQLi detection
    ├── xss_checker.py          ← XSS detection
    ├── csrf_checker.py         ← CSRF detection
    └── advanced_checker.py    ← Headers / Files / Redirect / Ports
```

## ⚡ Quick Setup & Run

### Step 1: Install Python
Make sure Python 3.10+ is installed: https://python.org

### Step 2: Open Terminal / CMD in the `cyber_wings` folder

```bash
cd cyber_wings
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the app

```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## 🔍 Features

| Module | Description |
|--------|-------------|
| 🔒 SSL Analyzer | Certificate validity, expiry, cipher, TLS version, grading |
| 💉 SQL Injection | Error-based & time-based blind SQLi detection |
| ⚡ XSS Scanner | Reflected XSS with CSP header analysis |
| 🛡️ CSRF Scanner | Form token audit, SameSite cookies, CORS check |
| 🔍 Advanced | Security headers, sensitive files, open redirect, port scan |
| 👥 About Us | Team profiles — Cyber Wings, Vadodara |

---

## ⚠️ Ethical Use

This tool is for **educational and authorized testing purposes only**.  
Always obtain explicit permission before scanning any website.

---

**Cyber Wings** • Vadodara, Gujarat, India • 2025
