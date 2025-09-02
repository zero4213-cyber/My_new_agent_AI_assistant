# Intent detection module

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os
import logging # Thêm logging

# Dữ liệu huấn luyện sơ khởi
training_data = {
    "teaching": [
        "teach me", "how to learn python", "giảng bài", "học về AI", "dạy tôi",
        "tôi muốn học", "hướng dẫn tôi", "tài liệu học", "cách học"
    ],
    "security": [
        "scan system", "check for vulnerabilities", "quét lỗ hổng", "bảo mật thiết bị",
        "kiểm tra an ninh", "làm sao để bảo vệ", "hệ thống có an toàn không"
    ],
    "investment": [
        "stock price", "bitcoin value", "giá cổ phiếu", "nên đầu tư",
        "thông tin thị trường", "dự đoán chứng khoán", "giá vàng"
    ],
    "cve_lookup": [
        "check cve", "CVE-2021-1234", "lỗ hổng CVE", "tra cứu CVE", "CVE là gì",
        "thông tin lỗ hổng"
    ],
    "create_ai_child": [
        "create ai", "sinh ai con", "tạo ai chuyên biệt", "làm ai con mới",
        "tạo trợ lý ai riêng", "sinh ra một ai"
    ],
    "generate_ai": [
        "tạo ai mới", "generate ai assistant", "ai generator", "thiết kế ai",
        "lập trình ai", "xây dựng ai"
    ],
    "quet_cong": [
        "quét cổng", "kiểm tra cổng mở", "scan port", "cổng nào đang mở",
        "kiểm tra cổng ip"
    ],
    "mat_khau": [
        "kiểm tra mật khẩu", "độ mạnh mật khẩu", "mật khẩu an toàn",
        "password strength", "khóa mật khẩu"
    ],
    "bao_mat": [
        "an ninh mạng", "tấn công mạng", "phòng chống mã độc", "bảo mật thông tin",
        "hỏi về an ninh", "cách bảo vệ máy tính"
    ],
    "tai_lieu": [
        "tài liệu học tập", "tài liệu về", "tài liệu an ninh", "tài liệu AI",
        "sách về", "khóa học"
    ],
    "kich_hoat_bao_ve": [
        "bật bảo vệ", "kích hoạt bảo vệ", "chống tấn công", "bảo vệ hệ thống"
    ],
    "whois_ip": [
        "tra cứu ip", "whois domain", "thông tin ip", "kiểm tra tên miền",
        "ip này của ai"
    ],
    "summarize": [
        "tóm tắt bài", "tóm tắt văn bản", "tóm tắt tài liệu", "làm ơn tóm tắt"
    ],
    "review": [
        "ôn tập bài cũ", "gợi ý ôn tập", "review kiến thức", "bài cần ôn lại"
    ],
    "research": [
        "nghiên cứu về", "tìm kiếm thông tin", "tìm hiểu về", "tra cứu"
    ],
    "translate_on": [
        "bật dịch", "bật chế độ phiên dịch", "bật biên dịch"
    ],
    "translate_off": [
        "tắt dịch", "tắt chế độ phiên dịch", "tắt biên dịch"
    ],
    "translate_request": [
        "dịch câu này", "phiên dịch", "dịch sang tiếng anh", "dịch sang tiếng việt"
    ],
    "general_chat": [
        "xin chào", "bạn là ai", "bạn có khỏe không", "cảm ơn", "tạm biệt",
        "thời tiết hôm nay", "kể chuyện", "định nghĩa"
    ]
}

# Huấn luyện nếu chưa có mô hình
model_dir = "models/extensions" # Thay đổi thành một thư mục rõ ràng hơn
model_path = os.path.join(model_dir, "model_intent.pkl")
vectorizer_path = os.path.join(model_dir, "vectorizer_intent.pkl")

if not os.path.exists(model_dir):
    os.makedirs(model_dir)

model = None
vectorizer = None

if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
    logging.info("Đang huấn luyện mô hình phát hiện ý định...")
    corpus = []
    labels = []
    for label, phrases in training_data.items():
        corpus.extend(phrases)
        labels.extend([label] * len(phrases))

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    model = MultinomialNB()
    model.fit(X, labels)

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)
    logging.info("Đã huấn luyện và lưu mô hình phát hiện ý định.")
else:
    try:
        model = joblib.load(model_path)
        vectorizer = joblib.load(vectorizer_path)
        logging.info("Đã tải mô hình phát hiện ý định từ đĩa.")
    except Exception as e:
        logging.error(f"Lỗi khi tải mô hình phát hiện ý định: {e}. Có thể cần huấn luyện lại.")
        model = None # Reset model nếu tải thất bại
        vectorizer = None # Reset vectorizer nếu tải thất bại


def detect_intent(text):
    # Ưu tiên nhận diện từ khóa cho các ý định rõ ràng
    keywords = {
        "dạy": "teaching", "học": "teaching", "hướng dẫn": "teaching",
        "quét": "quet_cong", "scan": "quet_cong", "cổng": "quet_cong",
        "giá": "investment", "cổ phiếu": "investment", "đầu tư": "investment",
        "cve": "cve_lookup", "lỗ hổng": "cve_lookup", "vulnerability": "cve_lookup",
        "sinh ai con": "create_ai_child", "tạo ai con": "create_ai_child", "ai con": "create_ai_child",
        "tạo ai mới": "generate_ai", "generate ai": "generate_ai",
        "mật khẩu": "mat_khau", "password": "mat_khau", "độ mạnh": "mat_khau",
        "bảo mật": "bao_mat", "an ninh mạng": "bao_mat", "cyber security": "bao_mat",
        "tài liệu": "tai_lieu", "khóa học": "tai_lieu", "sách": "tai_lieu",
        "kích hoạt bảo vệ": "kich_hoat_bao_ve", "bật bảo vệ": "kich_hoat_bao_ve", "chống tấn công": "kich_hoat_bao_ve",
        "whois": "whois_ip", "tra cứu ip": "whois_ip", "thông tin ip": "whois_ip", "tên miền": "whois_ip",
        "tóm tắt": "summarize", "tóm gọn": "summarize",
        "ôn tập": "review", "ôn lại": "review", "gợi ý ôn": "review",
        "nghiên cứu": "research", "tìm kiếm": "research", "tra cứu": "research",
        "bật dịch": "translate_on", "bật phiên dịch": "translate_on",
        "tắt dịch": "translate_off", "tắt phiên dịch": "translate_off",
        "dịch": "translate_request", "phiên dịch": "translate_request"
    }

    text_lower = text.lower()
    for keyword, intent_name in keywords.items():
        if keyword in text_lower:
            logging.debug(f"Phát hiện ý định từ khóa: {intent_name} cho '{text}'")
            return intent_name

    # Fallback to ML model
    if model and vectorizer:
        try:
            text_vectorized = vectorizer.transform([text_lower])
            prediction = model.predict(text_vectorized)[0]
            logging.debug(f"Phát hiện ý định từ mô hình: {prediction} cho '{text}'")
            return prediction
        except Exception as e: # Catching specific model-related errors is better
            logging.error(f"Lỗi khi dự đoán ý định bằng mô hình: {e}")
            # Fallback to a default or general intent if model prediction fails
            return "general_chat"
    else:
        logging.warning("Mô hình phát hiện ý định hoặc vectorizer không được tải. Trả về ý định chung.")
        return "general_chat"