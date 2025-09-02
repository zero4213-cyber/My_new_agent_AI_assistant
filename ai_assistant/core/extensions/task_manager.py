tasks = {}

def add_task(task_id, description):
    if task_id in tasks:
        return f"[Task Manager] Tác vụ '{task_id}' đã tồn tại."
    tasks[task_id] = description
    return f"[Task Manager] Đã thêm tác vụ: {task_id} - {description}"

def stop_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return f"[Task Manager] Đã dừng và xóa tác vụ: {task_id}"
    return f"[Task Manager] Không tìm thấy tác vụ có ID: {task_id}"

def list_tasks():
    if not tasks:
        return "[Task Manager] Không có tác vụ nào đang hoạt động."
    return "\n".join([f"{tid}: {desc}" for tid, desc in tasks.items()])

