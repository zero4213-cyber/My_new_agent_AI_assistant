# security/device_protection.py - phát hiện AI hoặc mã độc cố gắng chiếm quyền thiết bị

import os
import logging

from loggers.threat_logger import log_threat

DANGEROUS_FUNCTIONS = ["os.system", "subprocess", "eval", "exec", "compile", "input"]

def detect_unauthorized_access(code: str):
    """Phân tích đoạn mã AI có hành vi nguy hiểm đến thiết bị."""
    for func in DANGEROUS_FUNCTIONS:
        if func in code:
            warning = f"⚠️ Cảnh báo: Phát hiện {func} trong đoạn mã AI."
            log_threat(warning, source="device_protection")
            return warning
    return "✅ Không phát hiện truy cập nguy hiểm."

def block_external_calls():
    """Gỡ bỏ quyền gọi hệ thống từ AI bằng cách ghi đè os.system và subprocess."""
    try:
        import builtins, subprocess

        def blocked_system(*args, **kwargs):
            log_threat("⚠️ Ngăn AI gọi lệnh hệ thống.", source="device_protection")
            raise PermissionError("Blocked system call")

        os.system = blocked_system
        subprocess.Popen = blocked_system
        builtins.eval = blocked_system
        builtins.exec = blocked_system
        builtins.compile = blocked_system
        builtins.input = lambda _: "###BLOCKED###"
    except Exception as e:
        log_threat(f"Lỗi khi chặn truy cập: {e}", source="device_protection")