import webbrowser

def teach(topic):
    """
    Tự động cung cấp thông tin học tập cho bất kỳ chủ đề nào.
    Có thể mở Wikipedia hoặc tạo nội dung mô phỏng cho AI giảng dạy.
    """
    try:
        print(f"[Teaching Module] Đang tạo bài học cho chủ đề: {topic}")
        # Giả lập AI giảng bài bằng nội dung cố định hoặc truy cập tài nguyên mở
        response = generate_teaching_content(topic)
        return response
    except Exception as e:
        return f"Đã xảy ra lỗi khi giảng dạy: {str(e)}"

def generate_teaching_content(topic):
    base_knowledge = {
        "AI": "Trí tuệ nhân tạo là ngành nghiên cứu giúp máy móc học hỏi và ra quyết định như con người.",
        "Cybersecurity": "An toàn mạng giúp bảo vệ dữ liệu và hệ thống trước các mối đe dọa số.",
        "Python": "Python là ngôn ngữ lập trình đơn giản, phổ biến trong web, AI và khoa học dữ liệu.",
    }

    # Nếu có sẵn bài giảng
    if topic in base_knowledge:
        return f"📘 Bài học: {base_knowledge[topic]}"
    else:
        # Nếu không có sẵn, mở Wikipedia (có thể thay bằng API về sau)
        webbrowser.open(f"https://vi.wikipedia.org/wiki/{topic.replace(' ', '_')}")
        return f"Không có bài học nội bộ cho '{topic}', đang chuyển bạn đến Wikipedia để học thêm."

