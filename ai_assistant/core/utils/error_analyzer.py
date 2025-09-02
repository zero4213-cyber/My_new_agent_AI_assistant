import re
from pathlib import Path

class ErrorAnalyzer:
    def __init__(self, log_file="logs/error.log"):
        self.log_file = Path(log_file)

    def analyze(self):
        """Đọc log và phân loại lỗi"""
        if not self.log_file.exists():
            return {}

        errors = {"ImportError": [], "NetworkError": [], "VoiceError": [], "Other": []}
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if "ModuleNotFoundError" in line:
                    errors["ImportError"].append(line.strip())
                elif "requests" in line or "aiohttp" in line:
                    errors["NetworkError"].append(line.strip())
                elif "speech" in line or "audio" in line:
                    errors["VoiceError"].append(line.strip())
                else:
                    errors["Other"].append(line.strip())
        return errors
