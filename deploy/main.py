# --- Giao diện Flask & SocketIO ---
from flask import Flask, render_template, request
from flask_socketio import SocketIO

# --- Gọi hệ thống xử lý trung tâm từ core ---
from core.main import start_ai_assistant

# --- Khởi tạo Flask app ---
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- ROUTES ---
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/avatar", methods=["GET"])
def avatar():
    return render_template("avatar_viewer.html")

@app.route("/ask", methods=["GET"])
def ask():
    q = request.args.get("q", "")
    if not q:
        return "❌ Bạn chưa nhập gì."
    
    # Bạn vẫn có thể xử lý sơ bộ ở đây hoặc gọi xử lý ở core nếu muốn
    return f"Bạn hỏi: {q}"

@app.route("/sync_github", methods=["GET"])
def sync_github():
    from ai_assistant.core.github_sync import upload_file_to_github
    import os
    logs_path = "ai_assistant/data/logs"
    for fname in os.listdir(logs_path):
        fpath = os.path.join(logs_path, fname)
        if os.path.isfile(fpath):
            upload_file_to_github(fpath, f"logs/{fname}", f"Manual sync {fname}")
    return "✅ Đã đồng bộ log lên GitHub."


# --- KHỞI ĐỘNG ---
if __name__ == "__main__":
    run_core_system()  # Khởi chạy toàn bộ AI mẹ từ core
    socketio.run(app, host="0.0.0.0", port=7860)
