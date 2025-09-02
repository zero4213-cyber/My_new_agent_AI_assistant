# models/init_models.py - khởi tạo các mô hình AI và công cụ sử dụng

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import faiss
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS

# Chatbot tổng quát
chatbot = pipeline("text-generation", model="bigscience/bloom-560m")

# Mô hình tóm tắt bài giảng
summarizer = pipeline("summarization", model="Falconsai/text_summarization")

# Phân tích cảm xúc
sentiment_pipeline = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

# Phát hiện nguy hiểm (đơn giản)
danger_predictor = pipeline("text-classification", model="unitary/toxic-bert")

# Bộ mã hóa ngữ nghĩa + FAISS memory
embedder = SentenceTransformer("all-MiniLM-L6-v2")
dimension = embedder.get_sentence_embedding_dimension()
index = faiss.IndexFlatL2(dimension)
memory_texts = []

# Mô hình phân tích công nghệ / thiết bị
tech_analyst = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

# Công cụ tìm kiếm web
search = DDGS()