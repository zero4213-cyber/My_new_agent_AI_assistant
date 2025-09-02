# features/device_design.py - thiết kế và mô phỏng thiết bị công nghệ

import os
import logging
from datetime import datetime

from graphviz import Digraph

from models.init_models import tech_analyst
from utils.error_logger import learn_from_failure
from storage.github_sync import upload_file_to_github

RECORDINGS_DIR = "recordings"

def propose_device_design(topic):
    """Đề xuất thiết kế thiết bị dựa trên công nghệ."""
    prompt = f"Hãy liệt kê các bước hoặc bộ phận cần thiết để thiết kế một thiết bị hoạt động theo nguyên lý công nghệ: '{topic}'. Trình bày từng mục trên một dòng riêng biệt."
    try:
        steps_raw = tech_analyst(prompt, max_length=300, do_sample=True, num_return_sequences=1)[0]["generated_text"]
        steps = [s.strip("- ").strip() for s in steps_raw.split("\n") if len(s.strip()) > 0]
        if not steps:
            steps = ["Không thể xác định các thành phần thiết bị."]
        return steps
    except Exception as e:
        logging.error(f"Lỗi khi đề xuất thiết kế thiết bị: {e}")
        learn_from_failure("propose_device_design", e)
        return ["Không thể đề xuất thiết kế do lỗi hệ thống."]

def generate_device_diagram(steps, filename_base="device_diagram"):
    """Tạo sơ đồ thiết bị dạng ảnh."""
    try:
        dot = Digraph(comment='Device Design Steps')
        dot.attr(rankdir='LR')
        for i, step in enumerate(steps):
            dot.node(str(i), step)
            if i > 0:
                dot.edge(str(i-1), str(i))
        filename = f"{filename_base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_path = dot.render(os.path.join(RECORDINGS_DIR, filename), format='png', cleanup=True)
        upload_file(output_path)
        return output_path
    except Exception as e:
        logging.error(f"Lỗi khi tạo sơ đồ ảnh: {e}")
        learn_from_failure("generate_device_diagram", e)
        return ""

def simulate_text_diagram(steps):
    """Tạo sơ đồ thiết bị dạng văn bản ASCII."""
    result = ""
    for i, step in enumerate(steps):
        if i > 0:
            result += "  ↓\n"
        result += f"[{step}]\n"
    return result