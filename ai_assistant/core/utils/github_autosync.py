
import os
from storage.github_sync import upload_file_to_github

def auto_sync_logs():
    logs_dir = "ai_assistant/data/logs"
    if os.path.exists(logs_dir):
        for fname in os.listdir(logs_dir):
            path = os.path.join(logs_dir, fname)
            if os.path.isfile(path):
                upload_file_to_github(path, f"logs/{fname}", f"Startup sync {fname}")
