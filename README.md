# My_new_agent_AI_assistant

Trợ lý AI đa năng, có khả năng:
- Giao tiếp hội thoại (text & voice).
- Học từ sai lầm và điều chỉnh hành vi.
- Thu thập và tóm tắt thông tin từ Internet.
- Hỗ trợ bảo mật, giám sát hệ thống & mạng.
- Dịch ngôn ngữ, đọc tin tức, kiểm tra tin giả.
- Sinh code, hỗ trợ giải thuật toán.

---
## ⚙️ Chức năng chính

### 1. Giao tiếp hội thoại
- Nhập lệnh qua **text** hoặc **voice**.
- Trả lời bằng text/giọng nói (pyttsx3 / gTTS).

### 2. Bộ não hội thoại (unified_chat)
- **Security Chat**: CVE scan, port scan, password check, firewall, IP/Whois.
- **General Chat**: dịch ngôn ngữ, tin tức, kiểm tra tin giả, nghiên cứu, giải thuật toán, sinh code.
- **Fallback**: Semantic Search → trả lời thông minh hơn khi chưa rõ lệnh.

### 3. Giám sát nền
- Giám sát hệ thống (CPU, RAM…).
- Giám sát mạng (network scan).
- Báo cáo định kỳ, cảnh báo nguy hiểm.

### 4. Học từ sai lầm
- Ghi nhận lỗi.
- Phân tích nguyên nhân.
- Điều chỉnh để tránh lặp lại.

### 5. Thu thập tri thức
- MultiSourceResearch: tìm dữ liệu từ nhiều nguồn.
- Summarizer: tóm tắt nội dung.
- Hỗ trợ nghiên cứu nhanh.

### 6. Bảo mật & an toàn
- Firewall guard.
- Chống reverse attack.
- Quét an ninh hệ thống/mạng.
---
pyinstaller --onefile main.py
---

## 🚀 Cách chạy

```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Chạy AI Assistant
python main.py


## 📂 Cấu trúc thư mục

```bash
ai_mother_full_combined_project_ready/
│
├── main.py
│   └── Entry point (khởi động AI, vòng lặp chính, unified_chat, background monitor)
│
├── ai_assistant/
│   │
│   ├── core/
│   │   ├── agent/
│   │   │   ├── chat.py
│   │   │   │   └── security_chat:
│   │   │   │       • Quét CVE
│   │   │   │       • Port scan
│   │   │   │       • Kiểm tra mật khẩu
│   │   │   │       • Firewall / bảo mật
│   │   │   │       • IP / Whois
│   │   │   │
│   │   │   └── semantic_engine.py
│   │   │       └── search_semantically (Semantic Search Fallback)
│   │   │
│   │   ├── extensions/
│   │   │   ├── security_defense.py
│   │   │   │   └── protect_from_reverse_hack, firewall_guard
│   │   │   ├── system_scan.py
│   │   │   │   └── system_monitor
│   │   │   └── network_scan.py
│   │   │       └── network_monitor
│   │   │
│   │   ├── tools/
│   │   │   └── (các công cụ phụ trợ: xử lý file, tiện ích CLI…)
│   │   │
│   │   └── utils/
│   │       └── (hàm hỗ trợ chung: logging, format dữ liệu…)
│   │
│   ├── modules/
│   │   ├── chat_response.py
│   │   │   └── general_chat:
│   │   │       • Dịch ngôn ngữ
│   │   │       • Tin tức
│   │   │       • Fake news detection
│   │   │       • Nghiên cứu
│   │   │       • Thuật toán / code support
│   │   │       • Fallback: Semantic Search → chờ lệnh
│   │   │
│   │   ├── learning_engine.py
│   │   │   └── learn_from_failure (ghi nhận, phân tích, điều chỉnh lỗi)
│   │   │
│   │   └── research_engine.py
│   │       ├── MultiSourceResearch.gather
│   │       └── Summarizer.summarize
│   │
│   └── __init__.py
│
├── requirements.txt
│   └── Các thư viện: pyaudio, speechrecognition, pyttsx3, gtts, sounddevice, numpy, nltk, faiss, requests...
│
└── (các file cấu hình khác nếu có: config.py, logger.py, …)
