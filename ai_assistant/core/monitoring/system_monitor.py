# monitoring/system_monitor.py - giám sát tài nguyên hệ thống và tối ưu GPU

import psutil
import logging
import torch

from agent.voice import speak
from utils.error_logger import learn_from_failure

def monitor_system_resources():
    """Giám sát và thông báo trạng thái CPU và RAM."""
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        message = f"CPU hiện tại sử dụng {cpu} phần trăm. RAM sử dụng {ram} phần trăm."
        print(message)
        speak(message)
        return {"cpu": cpu, "ram": ram}
    except Exception as e:
        logging.error(f"Lỗi khi theo dõi tài nguyên hệ thống: {e}")
        learn_from_failure("monitor_system_resources", e)
        return {}

def optimize_gpu_usage():
    """Tối ưu sử dụng GPU nếu khả dụng."""
    try:
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            speak("Đã tối ưu bộ nhớ GPU.")
            return True
        else:
            speak("Không tìm thấy GPU trên thiết bị.")
            return False
    except Exception as e:
        logging.error(f"Lỗi khi tối ưu GPU: {e}")
        learn_from_failure("optimize_gpu_usage", e)
        return False