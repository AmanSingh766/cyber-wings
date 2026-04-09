import requests
import socket
import time
import re
from urllib.parse import urlparse, urlencode

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CyberWings-Scanner/1.0)",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
}

# Security headers to check
SECURITY_HEADERS = {
    "Strict-Transport-Security": {
        "desc": "HSTS — Forces HTTPS connections",
        "risk": "High",
    },
    "X-Frame-Options": {
        "desc": "Clickjacking protection",
        "risk": "Medium",
    },
    "Content-Security-Policy": {
        "desc": "XSS & injection mitigation",
        "risk": "High",
    },
    "X-Content-Type-Options": {
        "desc": "MIME-sniffing protection",
        "risk": "Low",
    },
    "X-XSS-Protection": {
        "desc": "Legacy XSS filter (browsers)",
        "risk": "Low",
    },
    "Referrer-Policy": {
        "desc": "Controls referrer info leakage",
        "risk": "Low",
    },
    "Permissions-Policy": {
        "desc": "Controls browser feature access",
        "risk": "Low",
    },
    "Cache-Control": {
        "desc": "Caching directives",
        "risk": "Low",
    },
    "X-Powered-By": {
        "desc": "Server tech disclosure (should be ABSENT)",
        "risk": "Info",
        "should_be_absent": True,
    },
    "Server": {
        "desc": "Server software disclosure",
        "risk": "Info",
        "should_be_absent": False,
    },
}

# Sensitive files to probe
SENSITIVE_FILES = [
    ".env", ".env.local", ".env.production",
    ".git/config", ".git/HEAD",
    "config.php", "wp-config.php", "config.yml", "config.yaml",
    "database.yml", "settings.py", "local_settings.py",
    "backup.sql", "dump.sql", "db_backup.sql",
    "admin/", "administrator/", "phpmyadmin/", "pma/",
    "robots.txt", "sitemap.xml",
    "phpinfo.php", "info.php", "test.php",
    ".htaccess", ".htpasswd",
    "web.config",
    "README.md", "CHANGELOG.md",
    "composer.json", "package.json", "Gemfile",
    ".DS_Store",
    "crossdomain.xml", "clientaccesspolicy.xml",
]

# Open redirect test params
REDIRECT_PARAMS = [
    "redirect", "redirect_to", "redirect_url", "return", "return_to",
    "returnUrl", "returnurl", "next", "url", "goto", "target",
    "link", "callback", "continue", "destination", "redir",
    "forward", "location", "jump",
]

REDIRECT_PAYLOAD = "https://evil-site-test.com"

# Common ports
COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}


def check_security_headers(url: str) -> dict:
    result = {"present": {}, "missing": {}, "info_headers": {}, "score": 0, "grade": "F", "error": None}
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        h = resp.headers

        total_scored = 0
        earned = 0

        for header, meta in SECURITY_HEADERS.items():
            should_absent = meta.get("should_be_absent", False)
            value = h.get(header)

            if meta["risk"] == "Info":
                result["info_headers"][header] = {
                    "value": value or "Not Present",
                    "desc": meta["desc"],
                    "present": value is not None,
                }
                continue

            risk_weight = {"High": 30, "Medium": 20, "Low": 10}.get(meta["risk"], 10)
            total_scored += risk_weight

            if value:
                result["present"][header] = {"value": value, "desc": meta["desc"], "risk": meta["risk"]}
                earned += risk_weight
            else:
                result["missing"][header] = {"desc": meta["desc"], "risk": meta["risk"]}

        result["score"] = int((earned / total_scored) * 100) if total_scored else 0
        s = result["score"]
        result["grade"] = "A+" if s >= 90 else "A" if s >= 80 else "B" if s >= 70 else "C" if s >= 60 else "D" if s >= 50 else "F"

    except Exception as e:
        result["error"] = str(e)
    return result


def check_sensitive_files(url: str) -> dict:
    result = {"found": [], "not_found": [], "error": None, "critical_count": 0}
    base = url.rstrip("/")
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    CRITICAL = [".env", ".git/config", "wp-config.php", "backup.sql", "dump.sql", ".htpasswd", "phpinfo.php"]

    for path in SENSITIVE_FILES:
        test_url = f"{base_url}/{path}"
        try:
            resp = requests.get(test_url, headers=HEADERS, timeout=6, allow_redirects=False)
            is_critical = any(c in path for c in CRITICAL)

            if resp.status_code == 200:
                content_length = len(resp.content)
                file_info = {
                    "path": path,
                    "url": test_url,
                    "status": resp.status_code,
                    "size": content_length,
                    "critical": is_critical,
                    "content_preview": resp.text[:150].strip() if content_length < 5000 else "[Large file]",
                }
                result["found"].append(file_info)
                if is_critical:
                    result["critical_count"] += 1
            elif resp.status_code in [301, 302, 403]:
                result["found"].append({
                    "path": path,
                    "url": test_url,
                    "status": resp.status_code,
                    "size": 0,
                    "critical": False,
                    "content_preview": f"[Status {resp.status_code} — exists but restricted]",
                })
            else:
                result["not_found"].append(path)
        except requests.exceptions.RequestException:
            result["not_found"].append(path)

    return result


def check_open_redirect(url: str) -> dict:
    result = {"vulnerable": False, "vulnerable_params": [], "findings": [], "error": None, "tests_done": 0}
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    for param in REDIRECT_PARAMS:
        test_url = f"{base}?{param}={REDIRECT_PAYLOAD}"
        result["tests_done"] += 1
        try:
            resp = requests.get(test_url, headers=HEADERS, timeout=7, allow_redirects=False)
            loc = resp.headers.get("Location", "")

            if resp.status_code in [301, 302, 303, 307, 308] and "evil-site-test.com" in loc:
                result["vulnerable"] = True
                result["vulnerable_params"].append(param)
                result["findings"].append({
                    "type": "open_redirect",
                    "param": param,
                    "redirect_to": loc,
                    "message": f"Open redirect via param '{param}' — redirects to {loc}",
                })
        except requests.exceptions.RequestException:
            pass

    if not result["findings"]:
        result["findings"].append({"type": "info", "message": "No open redirect vulnerabilities detected."})

    return result


def check_ports(url: str) -> dict:
    result = {"open": [], "closed": [], "host": None, "error": None}
    try:
        parsed = urlparse(url)
        host = parsed.hostname or url.split("/")[0]
        result["host"] = host

        for port, service in COMMON_PORTS.items():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1.5)
                conn = sock.connect_ex((host, port))
                if conn == 0:
                    result["open"].append({"port": port, "service": service})
                else:
                    result["closed"].append({"port": port, "service": service})
                sock.close()
            except Exception:
                result["closed"].append({"port": port, "service": service})

    except Exception as e:
        result["error"] = str(e)

    return result
