import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CyberWings-Scanner/1.0)",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
}

CSRF_TOKEN_NAMES = [
    "csrf", "csrftoken", "_csrf", "csrf_token", "csrf-token",
    "xsrf", "xsrftoken", "_xsrf", "xsrf_token",
    "authenticity_token", "_token", "token",
    "__requestverificationtoken", "anti_csrf",
    "form_token", "nonce",
]


def check_csrf(url: str) -> dict:
    result = {
        "url": url,
        "vulnerable": False,
        "risk_level": "Low",
        "forms_found": 0,
        "forms_protected": 0,
        "forms_unprotected": 0,
        "form_details": [],
        "cookie_analysis": [],
        "cors_analysis": {},
        "findings": [],
        "error": None,
    }

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        body = resp.text
        resp_headers = resp.headers
        cookies = resp.cookies

        soup = BeautifulSoup(body, "html.parser")

        # --- Form Analysis ---
        forms = soup.find_all("form")
        result["forms_found"] = len(forms)

        for idx, form in enumerate(forms):
            form_info = {
                "form_id": idx + 1,
                "action": form.get("action", "Same page"),
                "method": form.get("method", "GET").upper(),
                "has_csrf_token": False,
                "token_field": None,
                "sensitive_fields": [],
            }

            # Check for CSRF token fields
            hidden_inputs = form.find_all("input", {"type": "hidden"})
            all_inputs = form.find_all("input")

            for inp in hidden_inputs + all_inputs:
                name = (inp.get("name") or "").lower()
                inp_id = (inp.get("id") or "").lower()
                for token_name in CSRF_TOKEN_NAMES:
                    if token_name in name or token_name in inp_id:
                        form_info["has_csrf_token"] = True
                        form_info["token_field"] = inp.get("name") or inp.get("id")
                        break

            # Check for sensitive inputs (password, email, etc.)
            for inp in all_inputs:
                inp_type = (inp.get("type") or "text").lower()
                if inp_type in ["password", "email", "text", "tel"]:
                    form_info["sensitive_fields"].append(inp_type)

            if form_info["method"] == "POST":
                if form_info["has_csrf_token"]:
                    result["forms_protected"] += 1
                else:
                    result["forms_unprotected"] += 1
                    result["vulnerable"] = True
                    result["findings"].append({
                        "type": "csrf_no_token",
                        "message": f"Form #{idx+1} (POST to '{form_info['action']}') has NO CSRF token",
                        "sensitive": bool(form_info["sensitive_fields"]),
                    })

            result["form_details"].append(form_info)

        if result["forms_found"] == 0:
            result["findings"].append({
                "type": "info",
                "message": "No HTML forms found on this page.",
            })

        # --- Cookie SameSite Analysis ---
        for cookie in cookies:
            samesite = getattr(cookie, "same_site", None) or "Not Set"
            secure = cookie.secure
            http_only = cookie.has_nonstandard_attr("HttpOnly")

            cookie_info = {
                "name": cookie.name,
                "secure": secure,
                "httponly": http_only,
                "samesite": samesite,
                "risk": "Low",
            }

            if samesite in ["Not Set", "None"]:
                cookie_info["risk"] = "High"
                result["findings"].append({
                    "type": "cookie_samesite",
                    "message": f"Cookie '{cookie.name}' has SameSite={samesite} — CSRF risk elevated",
                })
            elif samesite == "Lax":
                cookie_info["risk"] = "Medium"

            if not secure:
                result["findings"].append({
                    "type": "cookie_secure",
                    "message": f"Cookie '{cookie.name}' lacks Secure flag — may be sent over HTTP",
                })

            result["cookie_analysis"].append(cookie_info)

        # --- CORS Header Analysis ---
        acao = resp_headers.get("Access-Control-Allow-Origin", "Not Set")
        acac = resp_headers.get("Access-Control-Allow-Credentials", "Not Set")

        result["cors_analysis"] = {
            "allow_origin": acao,
            "allow_credentials": acac,
        }

        if acao == "*":
            result["findings"].append({
                "type": "cors_wildcard",
                "message": "Access-Control-Allow-Origin: * — Any origin can make cross-origin requests",
            })
            result["vulnerable"] = True

        if acao == "*" and acac == "true":
            result["findings"].append({
                "type": "cors_critical",
                "message": "CRITICAL: Wildcard ACAO with credentials=true — Severe CSRF/CORS misconfiguration",
            })

        # --- Risk Level ---
        if result["vulnerable"]:
            if result["forms_unprotected"] > 1 or acao == "*":
                result["risk_level"] = "High"
            else:
                result["risk_level"] = "Medium"

        if not result["findings"]:
            result["findings"].append({
                "type": "info",
                "message": "No obvious CSRF vulnerabilities detected.",
            })

    except requests.exceptions.Timeout:
        result["error"] = "Request timed out. Check URL and try again."
    except requests.exceptions.ConnectionError:
        result["error"] = "Could not connect to the server."
    except Exception as e:
        result["error"] = f"Scanner error: {str(e)}"

    return result
