# core/translation.py - chứa các chức năng dịch thuật song ngữ

import os
import sys
import logging
import platform # Thêm import platform để kiểm tra hệ điều hành

from gtts import gTTS
from googletrans import Translator, LANGUAGES

from agent.voice import speak, listen
from utils.error_logger import learn_from_failure

RECORDINGS_DIR = "recordings"
# Tạo thư mục RECORDINGS_DIR nếu chưa tồn tại
if not os.path.exists(RECORDINGS_DIR):
    os.makedirs(RECORDINGS_DIR)

translator = Translator()
translation_mode = False

def toggle_translation_mode(status):
    """Bật/tắt chế độ phiên dịch."""
    global translation_mode
    translation_mode = status
    if status:
        speak("Đã bật chế độ phiên dịch. Tôi sẽ dịch mọi thứ bạn nói từ giờ.")
    else:
        speak("Đã tắt chế độ phiên dịch.")

def handle_translation_request(phrase):
    """Xử lý yêu cầu dịch thuật."""
    if not phrase or not phrase.strip():
        speak("Không nhận được giọng nói để phiên dịch.")
        return

    logging.info(f"Yêu cầu phiên dịch: '{phrase}'")
    try:
        detect = translator.detect(phrase)
        src_lang = detect.lang
        logging.info(f"Ngôn ngữ gốc phát hiện: {LANGUAGES.get(src_lang, src_lang)} ({src_lang})")

        target_lang = "en" if src_lang == "vi" else "vi"
        
        translated_obj = translator.translate(phrase, dest=target_lang)
        translated_text = translated_obj.text
        
        speak(f"Bản dịch tiếng {LANGUAGES.get(target_lang, target_lang)} là: {translated_text}")
        
        try:
            tts = gTTS(text=translated_text, lang=target_lang) 
            temp_file = os.path.join(RECORDINGS_DIR, "temp_translation.mp3")
            tts.save(temp_file)
            
            # Phần này đã được điều chỉnh để hỗ trợ Android (thông qua Linux)
            if platform.system() == "Windows":
                os.startfile(temp_file)
            elif platform.system() == "Linux": # Android thường báo là 'Linux'
                # Để điều này hoạt động trên Android (ví dụ với Termux), bạn cần cài đặt mpg123
                # Ví dụ: pkg install mpg123 trên Termux
                os.system(f"mpg123 {temp_file}")
            else:
                logging.warning(f"Hệ điều hành {platform.system()} không được hỗ trợ để phát âm trực tiếp.")
                speak("Xin lỗi, tôi không thể phát âm bản dịch trên hệ điều hành này.")
            
        except Exception as tts_e:
            logging.error(f"Lỗi khi phát âm bản dịch TTS: {tts_e}")
            speak("Xin lỗi, tôi không thể phát âm bản dịch lúc này.")
            learn_from_failure("gtts_play", tts_e)
    except Exception as e:
        logging.error(f"Lỗi khi phiên dịch câu '{phrase}': {e}")
        speak(f"Lỗi khi phiên dịch: {e}. Vui lòng thử lại.")
        learn_from_failure("handle_translation_request", e)