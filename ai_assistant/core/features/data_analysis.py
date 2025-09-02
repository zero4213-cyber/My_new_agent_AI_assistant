# features/data_analysis.py - phân tích dữ liệu từ file CSV

import os
import logging
import pandas as pd

from agent.voice import speak
from utils.error_logger import learn_from_failure

def analyze_data_from_csv(filepath="data.csv"):
    """Đọc và phân tích dữ liệu cơ bản từ file CSV."""
    try:
        df = pd.read_csv(filepath)
        info = {
            "số dòng": df.shape[0],
            "số cột": df.shape[1],
            "cột": list(df.columns),
            "mô tả": df.describe(include='all').to_dict()
        }
        return info
    except FileNotFoundError:
        speak(f"Không tìm thấy file {filepath}.")
        return {"error": f"Không tìm thấy file {filepath}."}
    except pd.errors.EmptyDataError:
        speak("File dữ liệu rỗng.")
        return {"error": "File dữ liệu rỗng."}
    except Exception as e:
        logging.error(f"Lỗi khi phân tích dữ liệu từ CSV: {e}")
        learn_from_failure("analyze_data_from_csv", e)
        return {"error": "Lỗi khi phân tích dữ liệu."}