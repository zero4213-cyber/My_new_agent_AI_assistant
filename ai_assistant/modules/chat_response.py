import re
from core.utils.logger import log_message, log_chat, log_user_action

# Import từ extensions
from core.extensions.semantic_search import search_semantically
from core.extensions.intent_detection import detect_intent
from core.extensions.cybersecurity_tools import check_cve, suggest_owasp_learning
from core.extensions.teaching_module import teach
from core.extensions.ai_child_manager import create_ai_child
from core.extensions.task_manager import add_task, stop_task
from core.extensions.network_lookup import whois_lookup, geoip_lookup
from core.extensions.security_defense import protect_against_reverse_attack
from core.extensions.avatar_effects import blink_and_glow
from core.extensions.learning_recommendation import recommend_learning_resources
from core.extensions.translation import translate_text
from core.extensions.summarize import summarize_text
from core.extensions.social_reply import generate_social_reply
from core.features.investment_analysis import get_stock_price, get_crypto_price, compare_stocks, suggest_investment
from core.features.fake_news import detect_fake_news
from core.features.sentiment import analyze_sentiment
from core.features.device_design import propose_device_design, generate_device_diagram, simulate_text_diagram
from core.features.visualization import visualize_data
from core.features.face_detection import detect_face_presence
from core.features.cve_lookup import search_cve
from core.features.ip_tools import whois_lookup as ip_whois_lookup, ip_lookup # Đổi tên whois_lookup để tránh trùng lặp
from core.features.data_analysis import analyze_data_from_csv
from core.features.security_learning import get_learning_resources
from core.features.cyber_assistant import answer_cyber_question, list_top_vulnerabilities
from core.monitoring.system_monitor import monitor_system_resources, optimize_gpu_usage
from core.monitoring.network_monitor import monitor_network_anomalies, monitor_outgoing_connections
from core.extensions.firewall_guard import check_firewall_rules, simulate_intrusion_detection, strengthen_firewall, protect_from_reverse_hack 
from core.extensions.recorder import record_audio, capture_image
from core.tools.network_scanner import scan_open_ports # Thêm dòng này
from core.agent.multi_source_research import MultiSourceResearch
from core.agent.summarizer import Summarizer
from core.features.software_assistant import SoftwareAssistant
from core.features.algorithm_solver import AlgorithmSolver

researcher = MultiSourceResearch()
summarizer = Summarizer()
software_helper = SoftwareAssistant()
algo_solver = AlgorithmSolver()

def chat_response(user_input: str):
    intent = detect_intent(user_input)
    user_input_lower = user_input.lower()

    if intent == "teaching" or "teach" in user_input_lower:
        return teach(user_input)
    elif intent == "security" or "scan" in user_input_lower:
        return protect_against_reverse_attack()
    elif intent == "investment" or any(x in user_input_lower for x in ["price", "giá", "stock", "crypto"]):
        if "so sánh" in user_input_lower:
            tokens = [t.upper() for t in user_input.split() if t.isalpha() and len(t) <= 5]
            if len(tokens) >= 2:
                return compare_stocks(tokens[0], tokens[1])
        for token in user_input.upper().split():
            if token in ["BTC", "ETH", "BNB", "DOGE", "SOL"]:
                return get_crypto_price(token)
            if token.isalpha() and len(token) <= 5:
                return get_stock_price(token)
        return suggest_investment()
    elif intent == "cve_lookup" or "cve" in user_input_lower:
        cve_match = re.search(r"CVE-\d{4}-\d{4,7}", user_input, re.IGNORECASE)
        if cve_match:
            return check_cve(cve_match.group())
        else:
            return "Please provide a valid CVE ID."
    elif intent == "create_ai_child" or "child ai" in user_input_lower:
        return create_ai_child(user_input)

     # === CÁC LỆNH LIÊN QUAN ĐẾN IP (Sử dụng kết hợp 2 file) ===
    if "whois" in user_input_lower:
        domain_or_ip = user_input_lower.replace("whois", "").strip()
        if domain_or_ip:
            result = whois_lookup(domain_or_ip) # Gọi WHOIS từ network_lookup.py
            if isinstance(result, dict) and "error" not in result:
                formatted_result = f"Thông tin WHOIS cho {result.get('domain', domain_or_ip)}:\n"
                formatted_result += f"- Registrar: {result.get('registrar', 'N/A')}\n"
                formatted_result += f"- Creation Date: {result.get('creation_date', 'N/A')}\n"
                formatted_result += f"- Expiration Date: {result.get('expiration_date', 'N/A')}\n"
                formatted_result += f"- Name Servers: {', '.join(result.get('name_servers', ['N/A']))}\n"
                return formatted_result
            return result.get('error', "Không thể tra cứu WHOIS.") # Trả về lỗi nếu có
        return "Bạn muốn tra cứu WHOIS cho tên miền hoặc IP nào?"
    elif "geoip" in user_input_lower:
        ip_addr = user_input_lower.replace("geoip", "").strip()
        if ip_addr:
            result = geoip_lookup(ip_addr) # Gọi GeoIP từ network_lookup.py (cần GeoLite2-City.mmdb)
            if isinstance(result, dict) and "error" not in result:
                formatted_result = f"Thông tin GeoIP cho {result.get('ip', ip_addr)}:\n"
                formatted_result += f"- Quốc gia: {result.get('country', 'N/A')}\n"
                formatted_result += f"- Thành phố: {result.get('city', 'N/A')}\n"
                formatted_result += f"- Vĩ độ: {result.get('latitude', 'N/A')}\n"
                formatted_result += f"- Kinh độ: {result.get('longitude', 'N/A')}\n"
                return formatted_result
            return result.get('error', "Không thể tra cứu GeoIP.") # Trả về lỗi nếu có
        return "Bạn muốn tra cứu GeoIP cho địa chỉ IP nào?"
    elif "tra cứu ip" in user_input_lower or "ip lookup" in user_input_lower:
        # Lệnh mới để gọi ip_lookup từ ip_tools.py (thông tin chi tiết hơn)
        ip_addr = user_input_lower.replace("tra cứu ip", "").replace("ip lookup", "").strip()
        if ip_addr:
            info = ip_lookup(ip_addr) # ip_lookup đã trả về chuỗi được định dạng
            return info
        return "Vui lòng cung cấp địa chỉ IP để tra cứu."
    elif "ip công khai của tôi" in user_input_lower or "my public ip" in user_input_lower:
        # Lệnh mới để gọi get_public_ip từ ip_tools.py
        public_ip = get_public_ip()
        return public_ip # get_public_ip đã trả về chuỗi có thông báo hoặc lỗi

    elif "avatar" in user_input_lower or "blink" in user_input_lower:
        blink_and_glow()
        return "Avatar hiệu ứng đang thực hiện"
    elif "recommend learning" in user_input_lower:
        topic = user_input_lower.replace("recommend learning", "").strip()
        return recommend_learning_resources(topic)
    elif "translate" in user_input_lower:
        return translate_text(user_input)
    elif "summarize" in user_input_lower:
        return summarize_text(user_input)
    elif "fake news" in user_input_lower:
        return detect_fake_news(user_input)
    elif "social reply" in user_input_lower:
        return generate_social_reply(user_input)

    # Firewall Guard (Các lệnh thủ công)
    elif "kiểm tra tường lửa" in user_input_lower or "check firewall rules" in user_input_lower:
        rules = check_firewall_rules()
        return f"Các quy tắc tường lửa hiện tại: {', '.join(rules)}"
    elif "mô phỏng xâm nhập" in user_input_lower or "simulate intrusion" in user_input_lower:
        alert = simulate_intrusion_detection()
        return f"Mô phỏng phát hiện xâm nhập: {alert}"
    elif "tăng cường tường lửa" in user_input_lower or "strengthen firewall" in user_input_lower:
        response = strengthen_firewall()
        return response
    elif "bảo vệ chống tấn công ngược" in user_input_lower or "anti-reverse hack" in user_input_lower:
        # Hàm này được điều khiển bằng lệnh người dùng từ firewall_guard.py
        response = protect_from_reverse_hack()
        return response

# === NETWORK SCANNER (Thêm phần này vào) ===
    elif "quét cổng" in user_input_lower or "scan ports" in user_input_lower:
        ip_match = re.search(r"(?:quét cổng|scan ports)\s+([\d.]+)", user_input_lower)
        if ip_match:
            target_ip = ip_match.group(1)
            # Bạn có thể điều chỉnh dải cổng hoặc timeout tại đây nếu muốn
            open_ports = scan_open_ports(target_ip)
            if open_ports and open_ports[0] != "Không phát hiện cổng mở.":
                return f"Các cổng mở trên {target_ip}: {', '.join(map(str, open_ports))}"
            else:
                return f"Không phát hiện cổng mở nào trên {target_ip} hoặc không thể quét."
        else:
            return "Vui lòng cung cấp địa chỉ IP để quét cổng. Ví dụ: 'quét cổng 192.168.1.1'"

    # Phân tích cảm xúc
    elif "sentiment" in user_input_lower or "cảm xúc" in user_input_lower:
        text_to_analyze = user_input_lower.replace("sentiment", "").replace("cảm xúc", "").strip()
        if text_to_analyze:
            return analyze_sentiment(text_to_analyze)
        else:
            return "Bạn muốn tôi phân tích cảm xúc của câu nào?"

    # Thiết kế thiết bị
    elif "thiết kế thiết bị" in user_input_lower or "device design" in user_input_lower:
        topic = user_input_lower.replace("thiết kế thiết bị", "").replace("device design", "").strip()
        if topic:
            steps = propose_device_design(topic)
            diagram_path = generate_device_diagram(steps)
            text_diagram = simulate_text_diagram(steps)
            response = f"Các bước thiết kế:\n{text_diagram}\nSơ đồ đã được tạo và lưu: {diagram_path}"
            return response
        else:
            return "Bạn muốn tôi thiết kế thiết bị gì?"

    # Recorder
    elif "ghi âm" in user_input_lower:
        duration_match = re.search(r"ghi âm (\d+) giây", user_input_lower)
        duration = int(duration_match.group(1)) if duration_match else 5 # Mặc định 5 giây
        filename = record_audio(duration)
        return f"Đã ghi âm xong và lưu vào: {filename}" if filename else "Không thể ghi âm."
    elif "chụp ảnh" in user_input_lower or "capture image" in user_input_lower:
        filename = capture_image()
        return f"Đã chụp ảnh xong và lưu vào: {filename}" if filename else "Không thể chụp ảnh."

    # System Monitor (theo lệnh)
    elif "kiểm tra tài nguyên" in user_input_lower or "monitor system" in user_input_lower:
        resources = monitor_system_resources()
        if resources:
            return f"CPU hiện tại: {resources['cpu']}%, RAM hiện tại: {resources['ram']}%."
        return "Không thể kiểm tra tài nguyên hệ thống lúc này."
    elif "tối ưu gpu" in user_input_lower or "optimize gpu" in user_input_lower:
        if optimize_gpu_usage():
            return "Đã tối ưu hóa việc sử dụng GPU."
        return "Không tìm thấy GPU hoặc không thể tối ưu hóa."

    # Network Monitor (theo lệnh)
    elif "kiểm tra bất thường mạng" in user_input_lower or "network anomalies" in user_input_lower:
        anomalies = monitor_network_anomalies()
        if anomalies:
            return "Phát hiện các bất thường mạng sau:\n" + "\n".join(anomalies)
        return "Không phát hiện bất thường mạng đáng kể."
    elif "kiểm tra kết nối đi" in user_input_lower or "outgoing connections" in user_input_lower:
        connections = monitor_outgoing_connections()
        if connections:
            return "Các kết nối đi hiện tại:\n" + "\n".join(connections)
        return "Không có kết nối đi nào đáng chú ý."

    # Trực quan hóa dữ liệu
    elif "trực quan hóa dữ liệu" in user_input_lower or "visualize data" in user_input_lower:
        # Cần xác định file, cột X, Y và loại biểu đồ từ user_input
        # Đây là ví dụ đơn giản, bạn có thể cần parsing phức tạp hơn
        filepath_match = re.search(r"file\s+(.+?)(?:\s+x_col\s+(.+?))?(?:\s+y_col\s+(.+?))?(?:\s+type\s+(.+))?$", user_input_lower)
        if filepath_match:
            filepath = filepath_match.group(1).strip()
            x_col = filepath_match.group(2).strip() if filepath_match.group(2) else None
            y_col = filepath_match.group(3).strip() if filepath_match.group(3) else None
            plot_type = filepath_match.group(4).strip() if filepath_match.group(4) else "line"
            return visualize_data(filepath, x_col, y_col, plot_type)
        else:
            return "Vui lòng cung cấp tên file, cột X, cột Y và loại biểu đồ (line, bar, scatter) để trực quan hóa dữ liệu."

    # Nhận diện khuôn mặt
    elif "nhận diện khuôn mặt" in user_input_lower or "detect face" in user_input_lower:
        if detect_face_presence():
            return "Đã phát hiện khuôn mặt."
        else:
            return "Không phát hiện khuôn mặt."

    # Tra cứu CVE
    elif "tra cứu cve" in user_input_lower or "search cve" in user_input_lower:
        cve_id_or_keyword = user_input_lower.replace("tra cứu cve", "").replace("search cve", "").strip()
        if cve_id_or_keyword:
            return search_cve(cve_id_or_keyword)
        else:
            return "Vui lòng cung cấp mã CVE hoặc từ khóa để tra cứu."

    # Phân tích dữ liệu từ CSV
    elif "phân tích dữ liệu" in user_input_lower or "analyze data" in user_input_lower:
        filepath_match = re.search(r"file\s+(.+)", user_input_lower)
        if filepath_match:
            filepath = filepath_match.group(1).strip()
            info = analyze_data_from_csv(filepath)
            if "error" in info:
                return info["error"]
            else:
                return f"Phân tích dữ liệu từ {filepath}:\nSố dòng: {info['số dòng']}\nSố cột: {info['số cột']}\nCác cột: {', '.join(info['cột'])}"
        else:
            return "Vui lòng cung cấp tên file CSV để phân tích dữ liệu."

    # Gợi ý học liệu bảo mật
    elif "học về bảo mật" in user_input_lower or "security learning" in user_input_lower:
        topic = user_input_lower.replace("học về bảo mật", "").replace("security learning", "").strip()
        resources = get_learning_resources(topic if topic else "OWASP")
        return "Các tài liệu học:\n" + "\n".join(resources)

    # Trợ lý kiến thức an ninh mạng
    elif "câu hỏi bảo mật" in user_input_lower or "cyber question" in user_input_lower:
        question = user_input_lower.replace("câu hỏi bảo mật", "").replace("cyber question", "").strip()
        if question:
            return answer_cyber_question(question)
        else:
            return "Bạn có câu hỏi gì về an toàn thông tin không?"
    elif "owasp top 10" in user_input_lower or "lỗ hổng phổ biến" in user_input_lower:
        vulnerabilities = list_top_vulnerabilities()
        return "OWASP Top 10 các lỗ hổng bảo mật phổ biến:\n" + "\n".join(vulnerabilities)

    #Lệnh tự động thu thập thông tin
    elif "tìm" in user_input or "tra cứu" in user_input or "research" in user_input:
        results = researcher.gather(user_input)
        if not results:
            return "❌ Xin lỗi, tôi không tìm thấy thông tin."
        combined_text = " ".join(results)
        summary = summarizer.summarize(combined_text, max_len=150)
        return f"🔎 Kết quả tôi tìm thấy:\n{summary}"

    #Tính năng dành cho người đi theo ngành CNPM 
    elif "phân tích code" in user_input:
        return software_helper.explain_code("... đoạn code bạn nhập ...")

    #Giải thuật toán
    elif "giải thuật" in user_input or "sorting" in user_input:
        arr = [5,3,8,2,1]
        steps = algo_solver.solve_sorting(arr)
        return algo_solver.explain_sorting() + f"\n\n👉 Các bước: {steps}"

    # fallback
    return "🤔 Tôi chưa rõ lệnh này, bạn có thể thử cách khác."

    # Semantic search fallback
    return search_semantically(user_input)
