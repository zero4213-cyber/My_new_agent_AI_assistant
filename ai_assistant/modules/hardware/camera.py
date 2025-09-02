
def capture_and_process():
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            # Xử lý ảnh tại đây nếu cần
            cv2.imwrite("captured_image.jpg", frame)
            return "Ảnh đã được lưu thành captured_image.jpg"
        return "Không thể chụp ảnh"
    except Exception as e:
        return f"Lỗi camera: {e}"
