# features/cve_lookup.py - tra cứu lỗ hổng bảo mật theo mã CVE

import requests

def search_cve(keyword_or_id):
    """Tra cứu CVE từ NVD API hoặc CVE Search."""
    try:
        if keyword_or_id.upper().startswith("CVE-"):
            url = f"https://cve.circl.lu/api/cve/{keyword_or_id.upper()}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return f"{data.get('id')}: {data.get('summary')}"
            return "Không tìm thấy CVE theo ID."
        else:
            url = f"https://cve.circl.lu/api/search/{keyword_or_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                results = response.json().get("results", [])
                if not results:
                    return "Không tìm thấy CVE phù hợp."
                return "\n".join(f"{r['id']}: {r['summary'][:80]}..." for r in results[:5])
            return "Không thể tra cứu CVE."
    except Exception as e:
        return f"⚠️ Lỗi khi tra CVE: {e}"