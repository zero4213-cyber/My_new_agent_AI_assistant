# features/sentiment.py - phân tích cảm xúc từ văn bản

import logging
from models.init_models import sentiment_pipeline
from utils.error_logger import learn_from_failure

def analyze_sentiment(text):
    """Phân tích cảm xúc từ văn bản."""
    if not sentiment_pipeline:
        return "Không thể phân tích cảm xúc: mô hình không tải được."
    try:
        result = sentiment_pipeline(text)[0]
        label = result['label']
        score = result['score']

        if "positive" in label.lower():
            return f"Tôi cảm thấy bạn đang có cảm xúc tích cực với độ tin cậy {score:.2f}."
        elif "negative" in label.lower():
            return f"Tôi cảm thấy bạn đang có cảm xúc tiêu cực với độ tin cậy {score:.2f}."
        else:
            return f"Tôi cảm thấy bạn có vẻ trung lập với độ tin cậy {score:.2f}."
    except Exception as e:
        logging.error(f"Lỗi khi phân tích cảm xúc: {e}")
        learn_from_failure("analyze_sentiment", e)
        return "Không thể phân tích cảm xúc lúc này."