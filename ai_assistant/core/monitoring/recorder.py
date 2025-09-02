# monitoring/recorder.py - ghi âm và chụp ảnh từ webcam

import os
import logging
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
from datetime import datetime

from agent.voice import speak
from utils.error_logger import learn_from_failure

RECORDINGS_DIR = "recordings"

def record_audio(duration=5, filename=None):
    """Ghi âm từ microphone trong khoảng thời gian nhất định."""
    try:
        fs = 44100
        if not filename:
            filename = os.path.join(RECORDINGS_DIR, f"recorded_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
        speak(f"Bắt đầu ghi âm trong {duration} giây.")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        write(filename, fs, audio)
        speak(f"Đã ghi âm xong và lưu vào {filename}.")
        return filename
    except Exception as e:
        logging.error(f"Lỗi khi ghi âm: {e}")
        learn_from_failure("record_audio", e)
        return ""

def capture_image(filename=None):
    """Chụp ảnh từ webcam và lưu lại."""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            speak("Không thể mở camera.")
            return ""
        ret, frame = cap.read()
        cap.release()
        if not filename:
            filename = os.path.join(RECORDINGS_DIR, f"captured_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        if ret:
            cv2.imwrite(filename, frame)
            speak(f"Đã chụp ảnh và lưu vào {filename}.")
            return filename
        else:
            speak("Không thể chụp ảnh.")
            return ""
    except Exception as e:
        logging.error(f"Lỗi khi chụp ảnh: {e}")
        learn_from_failure("capture_image", e)
        return ""