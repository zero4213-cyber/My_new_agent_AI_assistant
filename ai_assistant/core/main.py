# main.py - điểm khởi động trợ lý AI đơn giản

# main.py - điểm khởi động trợ lý AI đơn giản

import threading
import time

from agent.voice import speak, listen
from agent.memory import add_to_memory
from agent.chat import chat_response as security_chat
from modules.chat_response import chat_response as general_chat
from hardware_manager import handle_hardware_command
from utils.helpers import detect_wake_command
from storage.history_manager import save_conversation
from utils.logger import log_chat, log_user_action
from utils.error_logger import learn_from_failure, log_error
from agent.translation import toggle_translation_mode, handle_traslation_request
from agent.summarize import summarize_lecture, suggest_review
from extensions.security_defense import protect_from_reverse_hack
from monitoring.system_monitor import monitor_system_resources
from monitoring.network_monitor import monitor_network_anomalies, monitor_outgoing_connections
from agent.research import smart_research, extract_web_text
from core.agent.multi_source_research import MultiSourceResearch
from core.agent.summarizer import Summarizer
from core.extensions.semantic_search import search_semantically  # THÊM import này

stop_event = threading.Event()
researcher = MultiSourceResearch()  # DI CHUYỂN lên đây
summarizer = Summarizer()  # DI CHUYỂN lên đây

def unified_chat(user_input: str):
    security_keywords = [
        "cve", "quét cổng", "scan", "mật khẩu", "password",
        "bảo mật", "firewall", "whois", "ip", "tài liệu an ninh"
    ]
    general_keywords = [
        "dịch", "translate", "tin tức", "news", "fake", "nghiên cứu",
        "research", "thuật toán", "algorithm", "code", "phần mềm"
    ]

    if any(kw in user_input.lower() for kw in security_keywords):
        return security_chat(user_input)
    elif any(kw in user_input.lower() for kw in general_keywords):
        return general_chat(user_input)
    else:
        # Fallback semantic search
        semantic_result = search_semantically(user_input)
        if semantic_result and semantic_result[0] != "❌ Không tìm thấy kết quả ngữ nghĩa phù hợp.":
            return semantic_result[0]
        else:
            return "🤔 Tôi chưa hiểu lệnh này. Bạn có thể thử:\n- Câu hỏi bảo mật (CVE, scan, firewall...)\n- Câu hỏi chung (dịch, tin tức, research...)"

def respond_to_user_input(user_input: str):
    response = unified_chat(user_input)
    print("AI:", response)
    return response

def start_ai_assistant():
    """Khởi động trợ lý AI và xử lý các tương tác chính."""
    speak("Xin chào, tôi là trợ lý AI. Bạn cần gì?")

    print("Đang kích hoạt các tính năng bảo mật ban đầu...")
    initial_security_status = protect_from_reverse_hack()
    print(f"Trạng thái bảo mật ban đầu: {initial_security_status}")
    speak("Các hệ thống bảo mật đã được khởi động.")

    while not stop_event.is_set():
        try:
            user_input = listen()
            if not user_input:
                continue
            print(f"👤 Bạn: {user_input}")

            if detect_wake_command(user_input):
                speak("Tôi đang lắng nghe bạn đây.")
                continue

            if "tắt ai" in user_input.lower() or "shutdown assistant" in user_input.lower():
                speak("Tạm ")
                stop_event.set()
                break
            
            response = respond_to_user_input(user_input)
            speak(response)
            save_conversation(user_input, response)
            add_to_memory(response)
        except KeyboardInterrupt:
            speak("Được thôi. Tôi đang tắt các hệ thống. Tạm biệt!")
            stop_event.set()
            break
        except Exception as e:
            print(f"Lỗi trong vòng lặp chính của AI: {e}")
            learn_from_failure("main_loop_error", e)
            speak("Xin lỗi, tôi gặp một vấn đề. Vui lòng thử lại.")

def background_system_and_network_monitor():
    """Chức năng giám sát hệ thống và mạng chạy ngầm."""
    print("Khởi động giám sát tài nguyên hệ thống và mạng ngầm...")
    SYSTEM_MONITOR_INTERVAL = 300
    NETWORK_MONITOR_INTERVAL = 600

    last_system_check = time.time()
    last_network_check = time.time()

    while not stop_event.is_set():
        current_time = time.time()
        
        try:
            if current_time - last_system_check >= SYSTEM_MONITOR_INTERVAL:
                resources = monitor_system_resources()
                if resources:
                    if resources['cpu'] > 80:
                        speak("Cảnh báo: CPU đang sử dụng rất cao!")
                        log_user_action(f"CPU usage alert: {resources['cpu']}%")
                    if resources['ram'] > 80:
                        speak("Cảnh báo: RAM đang sử dụng rất cao!")
                        log_user_action(f"RAM usage alert: {resources['ram']}%")
                last_system_check = current_time

            if current_time - last_network_check >= NETWORK_MONITOR_INTERVAL:
                anomalies = monitor_network_anomalies()
                if anomalies:
                    speak("Cảnh báo: Phát hiện hoạt động mạng bất thường!")
                    log_user_action(f"Network anomaly alert: {anomalies}")
                    for anomaly in anomalies:
                        print(f"Mạng bất thường: {anomaly}")
                last_network_check = current_time

            time.sleep(10)

        except Exception as e:
            print(f"Lỗi trong luồng giám sát nền: {e}")
            learn_from_failure("background_monitor_error", e)

    print("Giám sát nền đã dừng.")
    
def background_research():
    """Chạy nền để lấy thông tin quan trọng định kỳ"""
    try:
        topics = ["CVE vulnerability", "stock market news", "AI safety news"]
        for topic in topics:
            results = researcher.gather(topic)
            if results:
                combined = " ".join(results)
                summary = summarizer.summarize(combined, max_len=100)
                print(f"⚠️ [CẢNH BÁO NỀN] Chủ đề: {topic}\n{summary}\n")
        threading.Timer(1800, background_research).start()
    except Exception as e:
        log_error(f"Background research error: {e}")

if __name__ == "__main__":
    background_research()  # Khởi chạy research nền
    ai_thread = threading.Thread(target=start_ai_assistant)
    ai_thread.start()

    monitor_thread = threading.Thread(target=background_system_and_network_monitor)
    monitor_thread.daemon = True
    monitor_thread.start()

    ai_thread.join()
    print("Chương trình đã thoát.")