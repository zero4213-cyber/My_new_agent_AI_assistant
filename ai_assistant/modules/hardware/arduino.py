
def connect_arduino(port='/dev/ttyUSB0', baudrate=9600):
    try:
        import serial
        ser = serial.Serial(port, baudrate, timeout=1)
        return ser
    except Exception as e:
        return f"Lỗi kết nối Arduino: {e}"
