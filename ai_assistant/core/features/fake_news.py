# features/fake_news.py - kiểm tra tin giả từ nội dung văn bản

def detect_fake_news(text):
    """Đánh giá sơ bộ tin tức có vẻ là giả hay không"""
    suspicious_keywords = ["giật gân", "tin nóng", "sốc", "kinh hoàng", "bị bắt", "âm mưu"]
    count = sum(word in text.lower() for word in suspicious_keywords)
    if count >= 2:
        return "Có dấu hiệu là tin giả"
    elif count == 1:
        return "Có thể là tin giả"
    else:
        return "Không có dấu hiệu tin giả"
