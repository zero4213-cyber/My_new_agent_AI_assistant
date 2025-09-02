# features/ip_tools.py - tra cứu WHOIS, IP public, và GeoIP

import requests

def whois_lookup(domain):
    """Truy vấn thông tin WHOIS của tên miền."""
    try:
        url = f"https://api.hackertarget.com/whois/?q={domain}"
        res = requests.get(url, timeout=5)
        return res.text if res.status_code == 200 else "Không thể tra cứu WHOIS."
    except Exception as e:
        return f"❌ Lỗi khi tra WHOIS: {e}"

def ip_lookup(ip_or_domain=""):
    """Trả về thông tin vị trí, ASN, tổ chức của IP."""
    try:
        query = ip_or_domain if ip_or_domain else ""
        url = f"http://ip-api.com/json/{query}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return f"🌍 IP: {data['query']}\nTổ chức: {data['org']}\nVị trí: {data['city']}, {data['country']}\nISP: {data['isp']}"
        return "Không thể tra IP."
    except Exception as e:
        return f"❌ Lỗi khi tra IP: {e}"