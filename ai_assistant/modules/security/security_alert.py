from core.agent.voice import speak
from core.utils.logger import log_message

def alert_user_on_threat(reason="Phát hiện hành vi nguy hiểm."):
    """Cảnh báo người dùng nếu phát hiện rủi ro an toàn."""
    message = f"⚠️ Cảnh báo: {reason} Vui lòng thận trọng."
    
    # Cảnh báo bằng giọng nói
    speak(message)
    
    # Ghi log để truy vết
    log_message(f"[SECURITY ALERT] {reason}")
    
    return {
        "status": "alert_triggered",
        "reason": reason
    }
