# core/research.py - nghiên cứu thông minh từ Wikipedia và web

import os
import json
import logging
from datetime import datetime

import wikipedia
import requests
from bs4 import BeautifulSoup

from models.init_models import search # Giả định 'search' là một công cụ tìm kiếm (ví dụ: DuckDuckGo)
from storage.google_drive import upload_file # Giả định hàm này tồn tại và hoạt động
from utils.error_logger import learn_from_failure

LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def smart_research(query):
    """Nghiên cứu thông tin từ Wikipedia và DuckDuckGo."""
    summary_wiki = ""
    try:
        # Có thể điều chỉnh số lượng câu từ Wikipedia
        summary_wiki = wikipedia.summary(query, sentences=5, auto_suggest=True, redirect=True)
        if not summary_wiki:
            summary_wiki = "Không tìm thấy bài Wikipedia hoặc bài quá ngắn."
    except wikipedia.exceptions.PageError:
        summary_wiki = f"Không tìm thấy bài Wikipedia cho '{query}'."
    except wikipedia.exceptions.DisambiguationError as e:
        # Gợi ý cho người dùng các lựa chọn khác
        options_text = ", ".join(e.options[:5])
        summary_wiki = f"Có nhiều kết quả cho '{query}'. Vui lòng cụ thể hơn. Các tùy chọn: {options_text}..."
    except Exception as e:
        logging.error(f"Lỗi khi tìm Wikipedia cho '{query}': {e}")
        learn_from_failure("wikipedia_search", e)
        summary_wiki = f"Đã xảy ra lỗi khi tìm kiếm Wikipedia: {e}"

    result_web = ""
    try:
        # Giả định search.run(query) trả về chuỗi kết quả tìm kiếm web
        web_raw_result = search.run(query)
        result_web = web_raw_result[:1000] if web_raw_result else "Không tìm thấy kết quả từ tìm kiếm web."
    except Exception as e:
        logging.error(f"Lỗi khi tìm DuckDuckGo cho '{query}': {e}")
        learn_from_failure("duckduckgo_search", e)
        result_web = f"Đã xảy ra lỗi khi tìm kiếm web: {e}"

    data = {
        "timestamp": datetime.now().isoformat(),
        "topic": query,
        "wiki_summary": summary_wiki,
        "web_result": result_web # Đã cắt bớt ở trên
    }
    file_path = os.path.join(LOGS_DIR, "research_history.json")

    # Đọc, cập nhật và ghi lại toàn bộ file JSON để đảm bảo cấu trúc hợp lệ
    all_research_entries = []
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    if content.startswith('[') and content.endswith(']'):
                        all_research_entries = json.loads(content)
                    else:
                        logging.warning(f"File {file_path} không có định dạng JSON mảng. Đang cố gắng sửa...")
                        try:
                            all_research_entries = [json.loads(content)]
                        except json.JSONDecodeError:
                            logging.error(f"File {file_path} bị hỏng, không thể đọc.")
                            all_research_entries = []
                else:
                    all_research_entries = []
        except json.JSONDecodeError as e:
            logging.error(f"Lỗi giải mã JSON từ {file_path}: {e}. File sẽ được ghi đè.")
            all_research_entries = []
        except Exception as e:
            logging.error(f"Lỗi khi đọc file lịch sử nghiên cứu: {e}")
            learn_from_failure("read_research_history_file", e)
            all_research_entries = []

    all_research_entries.append(data)

    try:
        with open(file_path, "w", encoding="utf-8") as f: # Ghi đè toàn bộ
            json.dump(all_research_entries, f, ensure_ascii=False, indent=2)
        upload_file(file_path)
    except Exception as e:
        logging.error(f"Lỗi khi lưu lịch sử nghiên cứu: {e}")
        learn_from_failure("save_research_history", e)

    return f"**Tóm tắt từ Wikipedia:**\n{summary_wiki}\n\n**Kết quả tìm kiếm web:**\n{result_web}"

def extract_web_text(url):
    """Trích xuất văn bản chính từ một trang web."""
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url # Thử thêm http nếu thiếu

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        r = requests.get(url, headers=headers, timeout=15) # Tăng timeout
        r.raise_for_status() # Ném ngoại lệ cho các mã trạng thái lỗi HTTP
        soup = BeautifulSoup(r.text, 'html.parser')

        # Thử các thẻ phổ biến chứa nội dung chính
        content_tags = ['p', 'h1', 'h2', 'h3', 'li', 'span']
        all_texts = []
        for tag_name in content_tags:
            for element in soup.find_all(tag_name):
                text = element.get_text(separator=' ', strip=True)
                if len(text) > 30: # Chỉ lấy các đoạn văn bản đủ dài
                    all_texts.append(text)

        # Giới hạn độ dài tổng thể của văn bản trích xuất
        full_text = '\n'.join(all_texts)
        if len(full_text) > 2000: # Tăng giới hạn lên 2000 hoặc hơn tùy nhu cầu
            full_text = full_text[:2000] + "..." # Thêm dấu "..." nếu bị cắt
        
        if not full_text.strip():
            return "Không thể trích xuất văn bản chính từ trang web này."

        return full_text
    except requests.exceptions.RequestException as e:
        logging.error(f"Lỗi khi truy cập trang web {url}: {e}")
        return f"Lỗi khi truy cập trang web: {e}. Vui lòng kiểm tra lại URL hoặc kết nối mạng."
    except Exception as e:
        logging.error(f"Không thể đọc hoặc phân tích trang web {url}: {e}")
        return f"Không thể đọc trang web: {e}. Có thể cấu trúc trang không cho phép trích xuất."