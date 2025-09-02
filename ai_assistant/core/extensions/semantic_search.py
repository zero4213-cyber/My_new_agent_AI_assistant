# Semantic search module

from difflib import get_close_matches

def search_semantically(query, database):
    """
    Tìm kiếm ngữ nghĩa bằng cách so khớp văn bản gần đúng.
    
    Args:
        query (str): Truy vấn đầu vào từ người dùng.
        database (list[str]): Danh sách nội dung hoặc khái niệm đã biết.

    Returns:
        list[str]: Danh sách kết quả gần giống nhất.
    """
    if not isinstance(database, list) or not database:
        return ["Cơ sở dữ liệu không hợp lệ hoặc rỗng."]

    matches = get_close_matches(query, database, n=3, cutoff=0.3)
    if matches:
        return [f"🔎 Kết quả phù hợp: {match}" for match in matches]
    else:
        return ["❌ Không tìm thấy kết quả ngữ nghĩa phù hợp."]
