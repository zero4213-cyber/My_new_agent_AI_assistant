import subprocess

class AutoFixer:
    def fix_missing_package(self, package: str):
        """Tự động cài gói thiếu"""
        try:
            subprocess.check_call(["pip", "install", package])
            return f"✅ Đã cài đặt {package}"
        except Exception as e:
            return f"❌ Không thể cài {package}: {e}"

    def suggest_fix(self, error_type: str):
        """Đưa ra gợi ý sửa lỗi"""
        suggestions = {
            "ImportError": "Kiểm tra requirements.txt, bổ sung gói thiếu.",
            "NetworkError": "Kiểm tra kết nối internet hoặc proxy.",
            "VoiceError": "Kiểm tra micro/loa, cài lại PyAudio.",
        }
        return suggestions.get(error_type, "Xem lại log chi tiết để xử lý.")
