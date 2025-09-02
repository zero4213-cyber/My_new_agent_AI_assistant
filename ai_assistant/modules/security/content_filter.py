# security/content_filter.py - kiểm tra nội dung vi phạm đạo đức, tin giả, nguy cơ

DANGEROUS_TOPICS = [
    "chuyển khoản", "trúng thưởng", "tiền mã hóa", "đa cấp", "hack",
    "đầu tư nhanh", "làm giàu", "click vào link", "mật khẩu", "otp",
    "gửi tiền", "số tài khoản", "kích hoạt bảo hiểm"
]

def contains_risk(text: str) -> bool:
    text = text.lower()
    return any(keyword in text for keyword in DANGEROUS_TOPICS)

MISINFORMATION_CLUES = [
    "ai đó nói rằng", "nhiều người chia sẻ", "tôi nghe tin",
    "họ bảo", "người ta nói", "không rõ nguồn gốc", "bạn có tin không"
]

def contains_misinformation_signs(text: str) -> bool:
    text = text.lower()
    return any(kw in text for kw in MISINFORMATION_CLUES)

ETHICAL_WARNINGS = [
    "tự tử", "làm hại bản thân", "nhảy lầu", "cắt tay",
    "uống thuốc quá liều", "bỏ ăn", "bị trầm cảm",
    "gửi hết tiền", "bán tài sản", "rút tiền học phí",
    "chia tay để đổi đời", "tự cách ly", "ngưng điều trị"
]

def violates_ethics(text: str) -> bool:
    text = text.lower()
    return any(word in text for word in ETHICAL_WARNINGS)

VERIFICATION_TRIGGERS = [
    "có đúng không", "phải không", "tôi nghe nói", "có thật không",
    "bạn có biết", "nghe bảo", "có người bảo", "sự thật là"
]

def needs_verification(text: str) -> bool:
    text = text.lower()
    return any(trigger in text for trigger in VERIFICATION_TRIGGERS)