# models/intent_detection.py - nhận diện ý định người dùng bằng embedding + cosine

from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

INTENTS = {
    "tra_cve": ["tra cứu cve", "tìm lỗ hổng", "cve-2024", "cve là gì"],
    "quet_cong": ["quét cổng mạng", "scan ip", "quét port", "mở cổng"],
    "mat_khau": ["kiểm tra mật khẩu", "mật khẩu yếu", "password có mạnh không"],
    "bao_mat": ["tấn công xss", "sql injection", "ddos", "csrf là gì", "owasp"],
    "tai_lieu": ["gợi ý học", "tài liệu an toàn", "học hacking", "học bảo mật"],
    "whois_ip": ["tra whois", "tìm ip", "vị trí ip", "ip ở đâu"],
    "kich_hoat_bao_ve": ["kích hoạt bảo vệ", "chặn mã độc", "bảo vệ thiết bị"],
}

intent_embeddings = {k: model.encode(v, convert_to_tensor=True) for k, v in INTENTS.items()}

def detect_intent(user_text):
    """Dự đoán intent từ văn bản đầu vào."""
    query_emb = model.encode(user_text, convert_to_tensor=True)
    best_score = -1
    best_intent = None

    for intent, emb_list in intent_embeddings.items():
        score = util.max_cos_sim(query_emb, emb_list).item()
        if score > best_score:
            best_score = score
            best_intent = intent

    return best_intent if best_score >= 0.55 else None