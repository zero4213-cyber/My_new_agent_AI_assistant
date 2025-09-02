# security/integrity_check.py - kiểm tra tính toàn vẹn tệp bằng mã hash

import os
import json
import hashlib
import logging
from datetime import datetime

from core.agent.voice import speak
from core.utils.error_logger import learn_from_failure
from core.storage.google_drive import upload_file

LOGS_DIR = "logs"

def compute_hash(file_path):
    """Tính mã hash SHA-256 của một tệp."""
    try:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Lỗi khi tính hash: {e}")
        learn_from_failure("compute_hash", e)
        return None

def verify_file_integrity(file_path, known_hash):
    """Kiểm tra tính toàn vẹn của tệp so với mã hash đã biết."""
    try:
        current_hash = compute_hash(file_path)
        if current_hash == known_hash:
            speak("Tệp không bị thay đổi.")
            return True
        else:
            speak("Tệp đã bị thay đổi hoặc bị xâm nhập.")
            return False
    except Exception as e:
        logging.error(f"Lỗi khi xác minh tính toàn vẹn: {e}")
        learn_from_failure("verify_file_integrity", e)
        return False

def check_file_integrity_periodically(file_path):
    """Ghi lại mã hash của file định kỳ để kiểm tra sau này."""
    try:
        hash_value = compute_hash(file_path)
        if not hash_value:
            return
        log_file = os.path.join(LOGS_DIR, "file_integrity_log.json")
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "hash": hash_value
        }
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
        upload_file(log_file)
    except Exception as e:
        logging.error(f"Lỗi khi ghi log hash file: {e}")
        learn_from_failure("check_file_integrity_periodically", e)