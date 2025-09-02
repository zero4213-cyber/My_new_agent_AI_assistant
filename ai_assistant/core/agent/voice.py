# core/voice.py - chứa các hàm liên quan đến voice input/output

import logging
import sys
import os
import threading
import speech_recognition as sr
import pyttsx3
import platform # Để kiểm tra hệ điều hành tốt hơn

from core.utils.error_logger import learn_from_failure

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty("rate", 170) # Tốc độ nói
    # Tùy chỉnh âm lượng (ví dụ: 0.9 = 90%)
    # engine.setProperty("volume", 0.9) 

    # Chọn giọng nữ nếu có
    voices = engine.getProperty("voices")
    female_voice = next((v for v in voices if "female" in v.name.lower() or "zira" in v.id.lower() or "vietnamese" in v.name.lower()), None)
    if female_voice:
        engine.setProperty("voice", female_voice.id)
        logging.info(f"Đã chọn giọng nói: {female_voice.name}")
    else:
        logging.warning("Không tìm thấy giọng nữ. Sử dụng giọng mặc định.")
except Exception as e:
    logging.error(f"Lỗi khởi tạo pyttsx3 engine: {e}")
    learn_from_failure("pyttsx3_init", e)
    engine = None # Đảm bảo engine là None nếu khởi tạo thất bại

recognizer = sr.Recognizer()

def speak(text):
    """Phát âm văn bản ra loa."""
    if not engine:
        logging.error("Engine phát âm chưa được khởi tạo hoặc bị lỗi.")
        print(f"AI: {text} (Không thể phát âm)")
        return

    print(f"AI: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        logging.error(f"Lỗi khi phát âm văn bản '{text[:50]}...': {e}")
        learn_from_failure("speak", e)

def listen():
    """Lắng nghe giọng nói từ microphone và chuyển thành văn bản."""
    with sr.Microphone() as source:
        print("🎧 Đang lắng nghe... (Vui lòng nói rõ ràng)")
        try:
            # Điều chỉnh độ nhạy cho tiếng ồn xung quanh trong một khoảng thời gian ngắn
            recognizer.adjust_for_ambient_noise(source, duration=0.5) 
            audio = recognizer.listen(source, timeout=7, phrase_time_limit=10) # Tăng timeout để linh hoạt hơn
        except sr.WaitTimeoutError:
            print("Không nhận được giọng nói trong thời gian quy định.")
            return ""
        except Exception as e:
            logging.error(f"Lỗi khi lắng nghe từ microphone: {e}")
            learn_from_failure("listen_microphone_error", e)
            return ""
            
    try:
        # Sử dụng Google Web Speech API cho tiếng Việt
        transcript = recognizer.recognize_google(audio, language="vi-VN")
        print(f"Bạn: {transcript}")
        return transcript
    except sr.UnknownValueError:
        print("Không thể nhận diện giọng nói. Vui lòng thử lại.")
        return ""
    except sr.RequestError as e:
        print(f"Lỗi kết nối với dịch vụ nhận dạng giọng nói; Vui lòng kiểm tra kết nối internet của bạn: {e}")
        learn_from_failure("listen_request_error", e)
        return ""
    except Exception as e:
        logging.error(f"Lỗi không xác định trong listen(): {e}")
        learn_from_failure("listen_unknown_error", e)
        return ""