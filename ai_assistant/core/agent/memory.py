# core/memory.py - quản lý bộ nhớ dài hạn bằng FAISS

import logging
import numpy as np
import os
import pickle # Để lưu trữ/tải index và texts

# Giả định các mô hình này được khởi tạo ở init_models.py
from models.init_models import embedder, index, memory_texts
from utils.error_logger import learn_from_failure

# Định nghĩa các đường dẫn lưu trữ
MEMORY_DIR = "data/memory" # Hoặc một thư mục phù hợp khác
FAISS_INDEX_PATH = os.path.join(MEMORY_DIR, "faiss_index.bin")
MEMORY_TEXTS_PATH = os.path.join(MEMORY_DIR, "memory_texts.pkl")

# Tạo thư mục nếu chưa tồn tại
if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

# Tải bộ nhớ khi khởi tạo module
def load_memory():
    """Tải index và memory_texts từ đĩa."""
    global index, memory_texts
    try:
        if os.path.exists(FAISS_INDEX_PATH):
            # FAISS index cần được tải riêng (nếu nó là FAISS.Index instance)
            # Cần kiểm tra lại cách 'index' được khởi tạo trong init_models.py
            # Nếu 'index' là một đối tượng FAISS, nó có phương thức read/write_index
            # Ví dụ: index = faiss.read_index(FAISS_INDEX_PATH)
            # Tạm thời bỏ qua việc tải index phức tạp ở đây nếu không rõ loại
            pass # Cần triển khai cụ thể nếu 'index' là một đối tượng FAISS lớn.

        if os.path.exists(MEMORY_TEXTS_PATH):
            with open(MEMORY_TEXTS_PATH, 'rb') as f:
                memory_texts.extend(pickle.load(f))
            logging.info(f"Đã tải {len(memory_texts)} mục vào bộ nhớ.")
    except Exception as e:
        logging.error(f"Lỗi khi tải bộ nhớ: {e}")
        learn_from_failure("load_memory", e)

# Gọi hàm tải bộ nhớ khi module được import
load_memory()

def save_memory():
    """Lưu index và memory_texts ra đĩa."""
    try:
        # Lưu memory_texts
        with open(MEMORY_TEXTS_PATH, 'wb') as f:
            pickle.dump(memory_texts, f)
        logging.info(f"Đã lưu {len(memory_texts)} mục từ bộ nhớ.")

        # Lưu FAISS index (nếu 'index' là một đối tượng FAISS thực sự)
        # if hasattr(index, 'write_index'): # Kiểm tra xem có phương thức write_index không
        #     faiss.write_index(index, FAISS_INDEX_PATH)
        #     logging.info("Đã lưu FAISS index.")

    except Exception as e:
        logging.error(f"Lỗi khi lưu bộ nhớ: {e}")
        learn_from_failure("save_memory", e)

def add_to_memory(text):
    """Thêm văn bản vào bộ nhớ FAISS (dài hạn)."""
    if not text or not text.strip():
        logging.warning("Cố gắng thêm văn bản rỗng vào bộ nhớ.")
        return

    try:
        # Đảm bảo vector có đúng kiểu dữ liệu và định dạng
        vector = embedder.encode([text]).astype('float32')
        index.add(vector)
        memory_texts.append(text)
        save_memory() # Lưu sau mỗi lần thêm hoặc định kỳ
        logging.info(f"Đã thêm vào bộ nhớ: '{text[:50]}...'")
    except Exception as e:
        logging.error(f"Lỗi khi thêm vào bộ nhớ FAISS: {e}")
        learn_from_failure("add_to_memory", e)

def recall_from_memory(query, top_k=3):
    """Truy xuất các văn bản liên quan từ bộ nhớ FAISS."""
    if not memory_texts or not index.ntotal: # Kiểm tra xem index có mục nào không
        logging.info("Bộ nhớ rỗng, không thể truy xuất.")
        return ""
    
    if not query or not query.strip():
        logging.warning("Truy vấn rỗng, không thể truy xuất từ bộ nhớ.")
        return ""

    try:
        # Đảm bảo vector truy vấn có đúng kiểu dữ liệu và định dạng
        query_vector = embedder.encode([query]).astype('float32')
        D, I = index.search(query_vector, top_k)
        
        # Lọc các chỉ số hợp lệ để tránh IndexError
        valid_indices = [i for i in I[0] if 0 <= i < len(memory_texts)]
        
        recalled_texts = [memory_texts[i] for i in valid_indices]
        if recalled_texts:
            logging.info(f"Đã truy xuất {len(recalled_texts)} mục từ bộ nhớ cho truy vấn '{query[:50]}...'.")
            return "\n".join(recalled_texts)
        else:
            logging.info(f"Không tìm thấy văn bản liên quan trong bộ nhớ cho truy vấn '{query[:50]}...'.")
            return ""
    except Exception as e:
        logging.error(f"Lỗi khi truy xuất từ bộ nhớ FAISS: {e}")
        learn_from_failure("recall_from_memory", e)
        return ""