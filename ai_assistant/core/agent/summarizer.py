from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text, max_len=100):
        return self.summarizer(text, max_length=max_len, min_length=30, do_sample=False)[0]['summary_text']
