# features/security_learning.py - gợi ý học liệu chuyên sâu về an toàn, an ninh mạng

def get_learning_resources(topic="OWASP"):
    """Trả về danh sách tài nguyên học theo chủ đề an toàn mạng."""
    topic = topic.lower()
    if "owasp" in topic:
        return [
            "📚 OWASP Official: https://owasp.org",
            "📘 OWASP Top 10 Guide: https://owasp.org/www-project-top-ten/",
            "🎓 OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org"
        ]
    elif "malware" in topic or "mã độc" in topic:
        return [
            "🔬 Malware Analysis 101: https://www.malware-traffic-analysis.net",
            "📘 Practical Malware Analysis (PDF/book)",
            "🔐 VirusShare: https://virusshare.com"
        ]
    elif "hacking" in topic:
        return [
            "🎓 Hack The Box: https://www.hackthebox.com",
            "🧠 TryHackMe: https://tryhackme.com",
            "📘 The Web Application Hacker's Handbook"
        ]
    elif "pentest" in topic:
        return [
            "🛠️ Offensive Security OSCP: https://www.offensive-security.com",
            "📄 Penetration Testing Execution Standard: https://www.pentest-standard.org",
            "📚 Kali Linux Tools: https://tools.kali.org"
        ]
    else:
        return [
            "📚 OWASP: https://owasp.org",
            "🎓 TryHackMe: https://tryhackme.com",
            "🔐 Practical Malware Analysis",
            "🧠 Hack The Box: https://www.hackthebox.com"
        ]