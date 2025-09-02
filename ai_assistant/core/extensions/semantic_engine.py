from difflib import get_close_matches

def match(text, knowledge_base=None):
    """
    Tìm kiếm ngữ nghĩa cơ bản bằng cách so khớp văn bản gần đúng trong cơ sở tri thức.
    """
    if knowledge_base is None:
        knowledge_base = [
            "Tấn công mạng",
            "Mã hóa dữ liệu",
            "Bảo vệ mật khẩu",
            "AI trong an ninh mạng",
            "Tường lửa và IDS",
            "Lỗ hổng OWASP",
            "Malware và ransomware"
        ]

    matches = get_close_matches(text, knowledge_base, n=3, cutoff=0.3)
    if matches:
        return f"Tôi tìm thấy những chủ đề liên quan: {', '.join(matches)}"
    return "Xin lỗi, tôi không tìm thấy chủ đề liên quan nào phù hợp."
