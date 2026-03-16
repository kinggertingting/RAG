# Model
import os


EMBEDDING_MODEL = "intfloat/multilingual-e5-small"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
LLM_MODEL = 'qwen2.5-1.5b-q4'
# LLM_MODEL = 'qwen2.5-1.5b-q4.gguf'

TOP_K = 5
RERANK_TOP_N = 3
SCORE_THRESHOLD = 0.6
# Chunking
CHUNK_SIZE = 500
OVERLAP = 50
MAX_CHUNKS = 2000

#Vector Database
QDRANT_HOST = "qdrant"
# QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = 'rag-collection'
VECTOR_DIM = 384 # Reuired by EMBEDDING_MODEL

#LLM
# LLM_BASE_URL = "http://localhost:8080/v1"
LLM_BASE_URL = "http://llama-server:8080/v1"


# Loader
MAX_FILE_SIZE_MB = 100
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".doc"}