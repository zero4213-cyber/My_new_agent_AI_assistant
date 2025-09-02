# loggers/threat_logger.py - ghi log mối đe dọa hoặc cảnh báo an ninh

import os
from datetime import datetime

LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

def log_threat(message, source="AI Security Monitor"):
    """Ghi lại thông tin cảnh báo vào file log."""
    entry = f"[{datetime.now().isoformat()}] ({source}) {message}\n"
    with open(os.path.join(LOGS_DIR, "threat_log.txt"), "a", encoding="utf-8") as f:
        f.write(entry)