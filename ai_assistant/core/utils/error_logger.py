from storage.github_sync import upload_file_to_github

# utils/error_logger.py - ghi nhận lỗi để học hỏi từ thất bại

import os
import json
from datetime import datetime

LOGS_DIR = "logs"

def learn_from_failure(context, error):
    """Lưu thông tin lỗi để học hỏi sau này."""
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "context": context,
        "error": str(error)
    }
    file_path = os.path.join(LOGS_DIR, "failure_log.json")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

# Cập nhật hàm log_error nếu tồn tại
def log_error(message: str):
    from datetime import datetime
    import os

    log_path = "data/logs.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"[{timestamp}] {message}\n"

    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(full_message)

    # Gọi GitHub upload sau mỗi log
    upload_file_to_github(log_path, "logs/logs.txt", f"Update log at {timestamp}")
