# Hướng dẫn kết nối phần cứng

## Arduino
- Kết nối Arduino qua cổng USB
- Dùng thư viện `pyserial` để giao tiếp
- Mã mẫu: `arduino_control.py`

## PLC
- Giao tiếp qua Modbus TCP hoặc RTU
- Dùng thư viện `pymodbus`
- Mã mẫu: `plc_connector.py`

## Camera
- Sử dụng OpenCV (`cv2.VideoCapture(0)`) để lấy hình ảnh từ webcam hoặc điện thoại
