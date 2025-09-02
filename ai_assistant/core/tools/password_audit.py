# tools/password_audit.py - kiểm tra độ mạnh và tính phổ biến của mật khẩu

import re

COMMON_PASSWORDS = {
    "123456", "password", "admin", "letmein", "qwerty", "12345678", "abc123", "admin123", "111111", "123123"
}

def check_password_strength(password):
    """Đánh giá độ mạnh mật khẩu và phát hiện mật khẩu yếu phổ biến."""
    if password in COMMON_PASSWORDS:
        return "❌ Mật khẩu quá phổ biến. Nên thay đổi ngay!"

    length = len(password) >= 8
    digit = re.search(r"\d", password)
    upper = re.search(r"[A-Z]", password)
    lower = re.search(r"[a-z]", password)
    symbol = re.search(r"[^a-zA-Z0-9]", password)

    score = sum([bool(length), bool(digit), bool(upper), bool(lower), bool(symbol)])
    if score == 5:
        return "✅ Mật khẩu mạnh."
    elif score >= 3:
        return "⚠️ Mật khẩu trung bình, nên cải thiện thêm."
    else:
        return "❌ Mật khẩu yếu, dễ bị tấn công."