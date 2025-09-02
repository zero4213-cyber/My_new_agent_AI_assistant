# storage/history_manager.py - lưu lại lịch sử trò chuyện và kiến thức

import os
import json
import logging
from datetime import datetime
from utils.error_logger import learn_from_failure
from storage.github_sync import upload_file_to_github  # ✅ Cập nhật đường dẫn mới

LOGS_DIR = "logs"

def save_conversation(input_text, response_text):
    """Lưu lại cuộc trò chuyện vào file JSON và tải lên GitHub."""
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        file_path = os.path.join(LOGS_DIR, "chat_history.json")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user": input_text,
            "assistant": response_text
        }
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # ✅ Upload lên GitHub
        upload_file_to_github(
            local_path=file_path,
            remote_path="logs/chat_history.json",
            commit_message="Auto-upload chat log"
        )

    except Exception as e:
        logging.error(f"Lỗi khi lưu lịch sử trò chuyện: {e}")
        learn_from_failure("save_conversation", e)


def save_learned_knowledge(new_knowledge):
    """Lưu kiến thức mới mà AI học được và tải lên GitHub."""
    try:
        os.makedirs(LOGS_DIR, exist_ok=True)
        file_path = os.path.join(LOGS_DIR, "learned_knowledge.json")
        entry = {
            "timestamp": datetime.now().isoformat(),
            "content": new_knowledge
        }
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        # ✅ Upload lên GitHub
        upload_file_to_github(
            local_path=file_path,
            remote_path="logs/learned_knowledge.json",
            commit_message="Auto-upload learned knowledge"
        )

    except Exception as e:
        logging.error(f"Lỗi khi lưu kiến thức học được: {e}")
        learn_from_failure("save_learned_knowledge", e)
