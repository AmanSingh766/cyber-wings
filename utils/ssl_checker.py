import ssl
import socket
import datetime
import hashlib
from urllib.parse import urlparse


def check_ssl(url: str) -> dict:
    result = {
        "url": url,
        "has_ssl": False,
        "error": None,
        "cert": {},
        "grade": "F",
        "issues": [],
        "recommendations": []
    }

    try:
        parsed = urlparse(url)
        hostname = parsed.hostname or url.replace("https://", "").replace("http://", "").split("/")[0]
        port = parsed.port or 443

        # Check if HTTP (no SSL)
        if parsed.scheme == "http":
            result["has_ssl"] = False
            result["error"] = "Website is using HTTP — no SSL/TLS encryption."
            result["issues"].append("No HTTPS — data is transmitted in plaintext")
            result["recommendations"].append("Enable HTTPS with a valid SSL certificate")
            result["grade"] = "F"
            return result

        ctx = ssl.create_default_context()
        conn = ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
        conn.settimeout(10)
        conn.connect((hostname, port))
        cert = conn.getpeercert()
        cipher = conn.cipher()
        protocol = conn.version()
        conn.close()

        result["has_ssl"] = True

        # Subject
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer  = dict(x[0] for x in cert.get("issuer",  []))

        # Expiry
        not_after  = datetime.datetime.strptime(cert["notAfter"],  "%b %d %H:%M:%S %Y %Z")
        not_before = datetime.datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
        days_left  = (not_after - datetime.datetime.utcnow()).days
        is_expired = days_left < 0

        # SANs
        sans = []
        for typ, val in cert.get("subjectAltName", []):
            if typ == "DNS":
                sans.append(val)

        # Serial number
        serial = cert.get("serialNumber", "N/A")

        result["cert"] = {
            "common_name":   subject.get("commonName", "N/A"),
            "organization":  subject.get("organizationName", "N/A"),
            "issuer_cn":     issuer.get("commonName", "N/A"),
            "issuer_org":    issuer.get("organizationName", "N/A"),
            "not_before":    not_before.strftime("%Y-%m-%d %H:%M UTC"),
            "not_after":     not_after.strftime("%Y-%m-%d %H:%M UTC"),
            "days_left":     days_left,
            "is_expired":    is_expired,
            "sans":          sans,
            "serial":        serial,
            "cipher_name":   cipher[0] if cipher else "N/A",
            "cipher_bits":   cipher[2] if cipher else 0,
            "tls_version":   protocol or "N/A",
            "hostname":      hostname,
        }

        # Grading
        score = 100

        if is_expired:
            result["issues"].append("Certificate has EXPIRED!")
            result["recommendations"].append("Renew your SSL certificate immediately")
            score -= 40
        elif days_left < 7:
            result["issues"].append(f"Certificate expires in {days_left} days — Critical!")
            result["recommendations"].append("Renew your SSL certificate urgently")
            score -= 25
        elif days_left < 30:
            result["issues"].append(f"Certificate expires soon ({days_left} days)")
            result["recommendations"].append("Plan SSL certificate renewal")
            score -= 10

        weak_protocols = ["TLSv1", "TLSv1.1", "SSLv2", "SSLv3"]
        if protocol in weak_protocols:
            result["issues"].append(f"Weak protocol in use: {protocol}")
            result["recommendations"].append("Upgrade to TLS 1.2 or TLS 1.3")
            score -= 20

        if cipher and cipher[2] and cipher[2] < 128:
            result["issues"].append(f"Weak cipher key length: {cipher[2]} bits")
            result["recommendations"].append("Use cipher suites with 128-bit or higher key length")
            score -= 15

        if not sans:
            result["issues"].append("No Subject Alternative Names (SAN) found")
            result["recommendations"].append("Add SAN entries for better browser compatibility")
            score -= 5

        if score >= 90:
            result["grade"] = "A+"
        elif score >= 80:
            result["grade"] = "A"
        elif score >= 70:
            result["grade"] = "B"
        elif score >= 60:
            result["grade"] = "C"
        elif score >= 50:
            result["grade"] = "D"
        else:
            result["grade"] = "F"

        if not result["issues"]:
            result["issues"] = ["No critical issues found"]

    except ssl.SSLCertVerificationError as e:
        result["has_ssl"] = True
        result["error"] = f"SSL Certificate Verification Failed: {str(e)}"
        result["issues"].append("Certificate verification failed — possibly self-signed or untrusted CA")
        result["recommendations"].append("Use a certificate from a trusted Certificate Authority (CA)")
        result["grade"] = "F"

    except ssl.SSLError as e:
        result["error"] = f"SSL Error: {str(e)}"
        result["grade"] = "F"

    except socket.timeout:
        result["error"] = "Connection timed out. Check the URL and try again."
        result["grade"] = "F"

    except socket.gaierror:
        result["error"] = "Hostname could not be resolved. Please check the URL."
        result["grade"] = "F"

    except ConnectionRefusedError:
        result["error"] = "Connection refused by the server on port 443."
        result["grade"] = "F"

    except Exception as e:
        result["error"] = f"Unexpected error: {str(e)}"
        result["grade"] = "F"

    return result
