import os
from datetime import datetime
from storage.github_sync import upload_file_to_github

LOG_BASE_PATH = "data/logs"

def log_message(module: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"{module}_log.txt"
    log_path = os.path.join(LOG_BASE_PATH, filename)
    full_message = f"[{timestamp}] {message}\n"

    os.makedirs(LOG_BASE_PATH, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(full_message)

    upload_file_to_github(log_path, f"logs/{filename}", f"[{module}] Update at {timestamp}")

def log_user_action(action: str):
    log_message("user_behavior", action)

def log_chat(query: str, response: str):
    combined = f"User: {query}\nAI: {response}\n"
    log_message("chat_history", combined)

# Ví dụ dùng thử
if __name__ == "__main__":
    log_message("network", "Đang quét các cổng TCP.")
    log_user_action("Người dùng mở trang phân tích CVE.")
    log_chat("Bạn là ai?", "Tôi là AI trợ lý của bạn.")
