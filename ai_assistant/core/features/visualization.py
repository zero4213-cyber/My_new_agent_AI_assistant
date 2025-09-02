# features/visualization.py - trực quan hóa dữ liệu từ CSV

import os
import logging
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from agent.voice import speak
from storage.github_sync import upload_file_to_github
from utils.error_logger import learn_from_failure

RECORDINGS_DIR = "recordings"

def visualize_data(filepath="data.csv", x_col=None, y_col=None, plot_type="line"):
    """Trực quan hóa dữ liệu từ file CSV thành đồ thị và lưu ảnh."""
    try:
        df = pd.read_csv(filepath)

        if not (x_col and y_col and x_col in df.columns and y_col in df.columns):
            speak("Vui lòng cung cấp tên cột X và Y hợp lệ để vẽ đồ thị.")
            return "Không đủ thông tin để vẽ đồ thị."

        plt.figure(figsize=(10, 6))

        if plot_type == "line":
            plt.plot(df[x_col], df[y_col])
            plt.title(f'Đồ thị đường của {y_col} theo {x_col}')
        elif plot_type == "bar":
            plt.bar(df[x_col], df[y_col])
            plt.title(f'Biểu đồ cột của {y_col} theo {x_col}')
        elif plot_type == "scatter":
            plt.scatter(df[x_col], df[y_col])
            plt.title(f'Biểu đồ phân tán của {y_col} theo {x_col}')
        else:
            speak("Loại đồ thị không được hỗ trợ. Chỉ hỗ trợ 'line', 'bar', 'scatter'.")
            return "Loại đồ thị không hỗ trợ."

        plt.xlabel(x_col)
        plt.ylabel(y_col)
        plt.grid(True)

        plot_filename = os.path.join(RECORDINGS_DIR, f"data_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        plt.savefig(plot_filename)
        plt.close()

        upload_file(plot_filename)
        speak(f"Đã tạo và lưu đồ thị vào {plot_filename}.")
        return f"Đồ thị đã được tạo và lưu."

    except FileNotFoundError:
        return f"Không tìm thấy file {filepath} để trực quan hóa."
    except Exception as e:
        logging.error(f"Lỗi khi trực quan hóa dữ liệu: {e}")
        learn_from_failure("visualize_data", e)
        return "Lỗi khi trực quan hóa dữ liệu."