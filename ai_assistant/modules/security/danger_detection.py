# security/danger_detection.py - dự đoán và xử lý nguy hiểm

import logging

from core.agent.voice import speak
from core.utils.error_logger import learn_from_failure

from core.models.init_models import danger_predictor

def predict_danger(text):
    """Dự đoán nguy cơ từ văn bản đầu vào."""
    try:
        result = danger_predictor(text)[0]
        label = result["label"]
        score = result["score"]
        if "toxic" in label.lower() or score > 0.8:
            return f"Cảnh báo nguy hiểm: {label} ({score:.2f})"
        else:
            return f"Không phát hiện nguy hiểm nghiêm trọng. ({label} - {score:.2f})"
    except Exception as e:
        logging.error(f"Lỗi khi phân tích nguy cơ: {e}")
        learn_from_failure("predict_danger", e)
        return "Không thể đánh giá nguy cơ lúc này."

def handle_danger(text):
    """Phản ứng khi phát hiện nguy cơ."""
    try:
        prediction = predict_danger(text)
        if "Cảnh báo" in prediction:
            speak("Cảnh báo! Có thể có nguy cơ nghiêm trọng trong nội dung vừa được phát hiện.")
        return prediction
    except Exception as e:
        logging.error(f"Lỗi khi xử lý nguy cơ: {e}")
        learn_from_failure("handle_danger", e)
        return "Không thể xử lý nguy cơ."