# core/summarize.py - tóm tắt bài giảng và gợi ý ôn tập

import os
import json
import logging
from datetime import datetime

from models.init_models import summarizer # Giả định 'summarizer' là một mô hình đã được khởi tạo
from agent.voice import speak
from storage.github_sync import upload_file # Giả định hàm này tồn tại và hoạt động
from utils.error_logger import learn_from_failure

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def summarize_lecture(text):
    """Tóm tắt văn bản dài."""
    # Chia nhỏ văn bản thành các đoạn nhỏ hơn để tóm tắt
    # Giả định mô hình 'summarizer' có giới hạn đầu vào.
    # Kích thước chunk có thể cần điều chỉnh tùy thuộc vào mô hình.
    chunk_size = 1000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for i, chunk in enumerate(chunks):
        try:
            # max_length và min_length nên được điều chỉnh phù hợp với yêu cầu tóm tắt
            summary_part = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
            summaries.append(summary_part)
        except Exception as e:
            logging.error(f"Lỗi khi tóm tắt một phần (chunk {i+1}): {e}")
            learn_from_failure("summarize_lecture_chunk", e)

    final_summary = " ".join(summaries)
    file_path = os.path.join(LOGS_DIR, "lecture_summaries.json")
    
    # Đọc, cập nhật và ghi lại toàn bộ file JSON để đảm bảo cấu trúc hợp lệ
    all_summaries = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    # Đảm bảo nội dung là một mảng JSON hợp lệ
                    if content.startswith('[') and content.endswith(']'):
                        all_summaries = json.loads(content)
                    else:
                        # Xử lý trường hợp file không phải là mảng JSON hợp lệ ban đầu
                        logging.warning(f"File {file_path} không có định dạng JSON mảng. Đang cố gắng sửa...")
                        try:
                            # Thử bọc bằng dấu ngoặc vuông nếu chỉ có một đối tượng
                            all_summaries = [json.loads(content)]
                        except json.JSONDecodeError:
                            logging.error(f"File {file_path} bị hỏng, không thể đọc.")
                            all_summaries = [] # Khởi tạo rỗng để tránh lỗi
                else:
                    all_summaries = []
        except json.JSONDecodeError as e:
            logging.error(f"Lỗi giải mã JSON từ {file_path}: {e}. File sẽ được ghi đè.")
            all_summaries = [] # Reset nếu file bị lỗi JSON
        except Exception as e:
            logging.error(f"Lỗi khi đọc file tóm tắt: {e}")
            learn_from_failure("read_lecture_summary_file", e)
            all_summaries = []

    all_summaries.append({"timestamp": datetime.now().isoformat(), "original_start": text[:200], "summary": final_summary})

    try:
        with open(file_path, "w", encoding="utf-8") as f: # Mở ở chế độ 'w' để ghi đè toàn bộ
            json.dump(all_summaries, f, ensure_ascii=False, indent=2)
        upload_file(file_path) # Giả định upload_file xử lý việc này
    except Exception as e:
        logging.error(f"Lỗi khi lưu tóm tắt bài giảng: {e}")
        learn_from_failure("save_lecture_summary", e)
    return final_summary

def suggest_review():
    """Gợi ý các bài cần ôn tập từ bản tóm tắt đã lưu."""
    file_path = os.path.join(LOGS_DIR, "lecture_summaries.json")
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        speak("Không có bài nào để gợi ý ôn tập trong file tóm tắt.")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                speak("File tóm tắt rỗng.")
                return

            # Đảm bảo nội dung là một mảng JSON hợp lệ
            if content.startswith('[') and content.endswith(']'):
                summaries_raw = json.loads(content)
            else:
                logging.warning(f"File {file_path} không có định dạng JSON mảng. Đang cố gắng đọc...")
                try:
                    summaries_raw = [json.loads(content)] # Thử bọc nếu chỉ có một đối tượng
                except json.JSONDecodeError:
                    speak("File tóm tắt bị hỏng hoặc không đúng định dạng.")
                    logging.error(f"File {file_path} bị hỏng, không thể đọc JSON.")
                    learn_from_failure("load_summaries_json_error", "Corrupt JSON file")
                    return

        summaries = [s for s in summaries_raw if "summary" in s]

        if summaries:
            # Sắp xếp theo timestamp nếu có, để gợi ý các bài gần đây nhất
            summaries.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            speak("Dưới đây là một số bài bạn nên ôn tập gần đây:")
            for s in summaries[:3]: # Lấy 3 bài gần đây nhất
                # Đảm bảo chỉ đọc tối đa 200 ký tự để tránh quá dài
                speak(s["summary"][:200].replace('\n', ' ') + "...")
        else:
            speak("Không có bài nào để gợi ý ôn tập trong file tóm tắt.")
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logging.error(f"Lỗi khi gợi ý ôn tập: {e}")
        speak(f"Không có bài nào để gợi ý ôn tập hoặc file bị lỗi: {e}")
        learn_from_failure("suggest_review", e)
    except Exception as e:
        logging.error(f"Lỗi không xác định khi gợi ý ôn tập: {e}")
        speak(f"Đã xảy ra lỗi không mong muốn khi gợi ý ôn tập: {e}")
        learn_from_failure("suggest_review_unknown_error", e)