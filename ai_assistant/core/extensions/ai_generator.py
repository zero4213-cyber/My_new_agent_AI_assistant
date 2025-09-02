def create_specialized_ai(domain, functions=None):
    """
    Tạo AI con chuyên biệt cho một lĩnh vực cụ thể.
    Thêm các chức năng tuỳ chỉnh nếu được chỉ định.
    """
    if functions is None:
        functions = ["basic_chat", "knowledge_base"]  # mặc định nếu không chỉ định gì

    print(f"[AI Generator] Đang tạo AI con cho lĩnh vực: {domain}")
    print(f"[AI Generator] Các chức năng được gán: {functions}")

    ai_info = {
        "status": "success",
        "ai_name": f"AI_{domain.replace(' ', '_')}",
        "domain": domain,
        "modules": functions
    }

    return ai_info
