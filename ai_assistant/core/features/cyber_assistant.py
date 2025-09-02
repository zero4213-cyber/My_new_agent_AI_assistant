# features/cyber_assistant.py - trợ lý kiến thức an toàn, an ninh mạng

from transformers import pipeline

# Mô hình trả lời câu hỏi ngắn (dùng lại từ transformers)
qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

CYBER_CONTEXT = """
An toàn và an ninh mạng là lĩnh vực bảo vệ hệ thống máy tính, mạng, và dữ liệu khỏi bị xâm nhập, tấn công hoặc phá hoại.
Một số khái niệm cơ bản:
- DDoS (Tấn công từ chối dịch vụ phân tán): làm nghẽn tài nguyên hệ thống bằng lưu lượng lớn.
- SQL Injection: chèn mã SQL độc hại để chiếm quyền truy cập cơ sở dữ liệu.
- OWASP Top 10: danh sách 10 lỗ hổng web phổ biến nhất do tổ chức OWASP công bố.
- XSS: tấn công chèn mã script vào trang web.
- Firewall: tường lửa kiểm soát lưu lượng mạng ra/vào hệ thống.
- Antivirus: phần mềm chống virus/mã độc.
- Phishing: giả mạo để lừa người dùng cung cấp thông tin cá nhân.
"""

def answer_cyber_question(question):
    """Trả lời các câu hỏi liên quan đến an toàn thông tin và bảo mật."""
    try:
        result = qa_pipeline({
            "question": question,
            "context": CYBER_CONTEXT
        })
        if result["score"] < 0.3 or result["answer"].strip() == "":
            return "❓ Tôi chưa đủ thông tin để trả lời. Bạn có thể hỏi lại rõ hơn hoặc yêu cầu tra cứu CVE."
        return f"📘 {result['answer']}"
    except Exception as e:
        return f"⚠️ Lỗi khi trả lời câu hỏi: {e}"

def list_top_vulnerabilities():
    """Trả về danh sách OWASP Top 10 mới nhất (đơn giản hóa)."""
    return [
        "1. Broken Access Control",
        "2. Cryptographic Failures",
        "3. Injection (SQL, NoSQL...)",
        "4. Insecure Design",
        "5. Security Misconfiguration",
        "6. Vulnerable and Outdated Components",
        "7. Identification and Authentication Failures",
        "8. Software and Data Integrity Failures",
        "9. Security Logging and Monitoring Failures",
        "10. Server-Side Request Forgery (SSRF)"
    ]