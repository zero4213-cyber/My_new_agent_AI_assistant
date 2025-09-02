import os
import base64
import requests

# Cấu hình GitHub cá nhân
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Đặt biến môi trường này trước khi chạy
REPO_OWNER = "zero78207"
REPO_NAME = "My_new_AI_assistant_multitasking"
BRANCH = "main"

def upload_file_to_github(local_path, remote_path, commit_message="Auto upload from AI"):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{remote_path}"

    # Đọc file và mã hóa base64
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf-8")

    # Kiểm tra nếu file đã tồn tại để lấy SHA
    response = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = response.json()["sha"] if response.status_code == 200 else None

    data = {
        "message": commit_message,
        "content": content,
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha

    r = requests.put(url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if r.status_code in [200, 201]:
        print(f"✅ Uploaded {remote_path} to GitHub.")
    else:
        print(f"❌ Error uploading file: {r.status_code} - {r.text}")

# Ví dụ sử dụng
if __name__ == "__main__":
    upload_file_to_github("data/logs.txt", "logs/logs.txt", "Upload logs from AI assistant")
