
# --- Hardware Auto-Detection ---
from .hardware import arduino, plc, camera
# Không gọi is_arduino_connected, mà gọi connect_arduino() rồi kiểm tra kết nối
from .hardware import arduino, plc, camera

def detect_connected_hardware():
    detected = []
    if isinstance(arduino.connect_arduino(), object):
        detected.append("Arduino")
    if isinstance(plc.connect_plc(), object):
        detected.append("PLC")
    if "Ảnh đã được lưu" in camera.capture_and_process():
        detected.append("Camera")
    return detected

