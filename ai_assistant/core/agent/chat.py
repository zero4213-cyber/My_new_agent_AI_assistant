# core/chat.py - phản hồi thông minh dựa vào ý định người dùng

# Kiểm tra lại các đường dẫn import này cho phù hợp với cấu trúc project thực tế
# Nếu chat.py nằm trong thư mục 'core', các import này có thể là:
from models.init_models import chatbot
from models.intent_detection import detect_intent
from features.cyber_assistant import answer_cyber_question, list_top_vulnerabilities
from features.cve_lookup import search_cve
from tools.network_scanner import scan_open_ports
from tools.password_audit import check_password_strength
from features.security_learning import get_learning_resources
from security.device_protection import block_external_calls
from features.ip_tools import whois_lookup, ip_lookup

import re
import logging # Thêm logging để ghi lại lỗi chi tiết hơn

def chat_response(text):
    """Phản hồi AI theo ý định được phát hiện từ câu hỏi người dùng."""
    # Chuyển đổi văn bản sang chữ thường để chuẩn hóa đầu vào cho detect_intent
    intent = detect_intent(text.lower())
    logging.info(f"Phát hiện ý định: {intent} cho câu hỏi: '{text}'")

    if intent == "tra_cve":
        return search_cve(text)

    if intent == "quet_cong":
        ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
        if ip_match:
            ip_address = ip_match.group()
            logging.info(f"Đang quét cổng cho IP: {ip_address}")
            try:
                # Đảm bảo scan_open_ports trả về chuỗi hoặc xử lý phù hợp
                return f"🌐 Cổng mở: {scan_open_ports(ip_address)}"
            except Exception as e:
                logging.error(f"Lỗi khi quét cổng cho {ip_address}: {e}")
                return "❌ Đã xảy ra lỗi khi quét cổng."
        return "❌ Không phát hiện IP để quét. Vui lòng cung cấp địa chỉ IP."

    if intent == "mat_khau":
        # Cần một cách an toàn hơn để trích xuất mật khẩu.
        # Hiện tại, nó lấy tất cả sau dấu ':' cuối cùng.
        # Cần cân nhắc bảo mật khi xử lý mật khẩu thực tế.
        parts = text.split(":")
        if len(parts) > 1:
            pwd = parts[-1].strip()
            if pwd:
                return check_password_strength(pwd)
            return "Vui lòng cung cấp mật khẩu để kiểm tra."
        return "Vui lòng cung cấp mật khẩu để kiểm tra (ví dụ: 'kiểm tra mật khẩu: abcxyz')."


    if intent == "bao_mat":
        return answer_cyber_question(text)

    if intent == "tai_lieu":
        # Cải thiện cách trích xuất chủ đề
        topic_keywords = ["tài liệu về", "tài liệu học", "học về"]
        topic = ""
        for kw in topic_keywords:
            if kw in text.lower():
                topic = text.lower().split(kw, 1)[1].strip()
                break
        
        if not topic:
            # Fallback nếu không tìm thấy từ khóa rõ ràng
            topic = text.replace("tài liệu", "").replace("học", "").strip()

        if topic:
            logging.info(f"Đang tìm tài liệu học tập cho chủ đề: {topic}")
            resources = get_learning_resources(topic)
            if resources:
                return "Dưới đây là một số tài liệu học tập về " + topic + ":\n" + "\n".join(resources)
            return f"Không tìm thấy tài liệu học tập về '{topic}'."
        return "Vui lòng cho tôi biết bạn muốn tìm tài liệu về chủ đề gì."


    if intent == "kich_hoat_bao_ve":
        try:
            block_external_calls()
            return "✅ Đã bật bảo vệ thiết bị, chặn mã độc nguy hiểm."
        except Exception as e:
            logging.error(f"Lỗi khi kích hoạt bảo vệ thiết bị: {e}")
            return "❌ Đã xảy ra lỗi khi cố gắng kích hoạt bảo vệ thiết bị."

    if intent == "whois_ip":
        # Cải thiện logic trích xuất IP/domain
        # Ưu tiên các định dạng IP hoặc domain phổ biến
        ip_or_domain = None
        # Kiểm tra IP trước
        ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text)
        if ip_match:
            ip_or_domain = ip_match.group()
        else:
            # Nếu không phải IP, thử tìm domain
            # Regex này đơn giản, có thể cần phức tạp hơn cho các trường hợp edge
            domain_match = re.search(r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}\b", text.lower())
            if domain_match:
                ip_or_domain = domain_match.group()

        if ip_or_domain:
            logging.info(f"Đang thực hiện tra cứu WHOIS/IP cho: {ip_or_domain}")
            # Xác định đây là IP hay domain để gọi hàm thích hợp
            if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip_or_domain):
                return ip_lookup(ip_or_domain)
            return whois_lookup(ip_or_domain)
        return "❌ Không tìm thấy IP hoặc domain cần tra cứu. Vui lòng cung cấp địa chỉ IP hoặc tên miền hợp lệ."

    # fallback
    try:
        # Giả định chatbot trả về list of dict, và cần lấy 'generated_text'
        result = chatbot(text, max_length=100, do_sample=True)
        if result and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]["generated_text"]
        logging.warning(f"Chatbot trả về kết quả không mong muốn: {result}")
        return "🤖 Tôi chưa thể phản hồi điều này một cách chính xác."
    except Exception as e:
        logging.error(f"Lỗi khi chatbot phản hồi: {e}")
        return "🤖 Xin lỗi, tôi không thể phản hồi điều này lúc này do lỗi hệ thống."