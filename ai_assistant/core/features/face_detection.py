# features/face_detection.py - nhận diện khuôn mặt qua webcam

import cv2
import logging

from agent.voice import speak
from utils.error_logger import learn_from_failure

FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH) if FACE_CASCADE_PATH else None

def detect_face_presence():
    """Kiểm tra sự hiện diện của khuôn mặt qua camera."""
    if not face_cascade:
        logging.warning(f"Không tìm thấy file Haar Cascade tại: {FACE_CASCADE_PATH}. Không thể nhận diện khuôn mặt.")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logging.error("Không thể mở camera để nhận diện khuôn mặt.")
        return False

    ret, frame = cap.read()
    if not ret:
        cap.release()
        return False

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    cap.release()

    if len(faces) > 0:
        speak("Tôi phát hiện có khuôn mặt ở trước camera.")
        return True
    return False