# utils/helpers.py - các tiện ích nhỏ như nhận diện lệnh đánh thức và kiểm tra mật khẩu

import re

def detect_wake_command(text):
    """Phát hiện lệnh đánh thức trợ lý AI trong văn bản."""
    wake_words = ["trợ lý", "này", "hey ai", "hello ai", "ê trợ lý"]
    text_lower = text.lower()
    return any(word in text_lower for word in wake_words)

def check_password_strength(password):
    """Kiểm tra độ mạnh của mật khẩu."""
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[ @!#$%^&*()<>?/\|}{~:]", password) is None

    score = 5 - sum([length_error, digit_error, uppercase_error, lowercase_error, symbol_error])

    if score == 5:
        return "Mật khẩu rất mạnh."
    elif score >= 3:
        return "Mật khẩu tạm ổn, nên cải thiện thêm."
    else:
        return "Mật khẩu yếu, cần thay đổi."