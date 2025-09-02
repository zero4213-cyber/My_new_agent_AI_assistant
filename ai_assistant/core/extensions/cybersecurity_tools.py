# Cybersecurity utilities
import requests

def check_cve(cve_id):
    sample_db = {
        "CVE-2021-44228": {
            "description": "Log4Shell - RCE in Apache Log4j2",
            "severity": "Critical",
            "patch": "Upgrade to Log4j 2.17.0 or later"
        },
        "CVE-2020-1472": {
            "description": "Zerologon vulnerability in Netlogon",
            "severity": "High",
            "patch": "Install August 2020 security update"
        }
    }
    return sample_db.get(cve_id, {"description": "Not found", "severity": "Unknown", "patch": "N/A"})

def suggest_owasp_learning():
    return {
        "Injection": "https://owasp.org/www-community/attacks/SQL_Injection",
        "Broken Authentication": "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/",
        "Sensitive Data Exposure": "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
        "XSS": "https://owasp.org/www-community/attacks/xss/",
        "Security Misconfiguration": "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"
    }
