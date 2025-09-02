from transformers import pipeline

class SoftwareAssistant:
    def __init__(self):
        self.generator = pipeline("text-generation", model="gpt2")

    def explain_code(self, code: str):
        """Phân tích code và đưa ra giải thích cơ bản"""
        return f"📖 Phân tích đoạn code:\n{code}\n\n👉 Đoạn này có chức năng xử lý ... (cần fine-tune thêm để chi tiết)."

    def suggest_code(self, prompt: str):
        """Sinh code mẫu từ mô tả"""
        response = self.generator(prompt, max_length=150, num_return_sequences=1)
        return response[0]["generated_text"]
