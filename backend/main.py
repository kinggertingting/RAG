from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore
from retrieval.retriever import Retriever
from rerank.cross_encoder import CrossEncoderModel
from rerank.rerank import Reranker
from llm.llm_service import LLMService
from rag.rag_pipeline import RAGPipeline
from ingestion.ingestion_service import IngestionService
from ingestion.loader import Loader
from ingestion.cleaner import Cleaner
from ingestion.chunker import Chunker

from config.settings import *


def main():

    print("🔄 Loading models...")

    # Core components
    embedder = Embedder(EMBEDDING_MODEL)
    qdrant_store = QdrantStore(QDRANT_HOST, QDRANT_PORT)
    retriever = Retriever(embedder, qdrant_store)
    cross_encoder = CrossEncoderModel(RERANK_MODEL)
    reranker = Reranker(cross_encoder)
    llm_service = LLMService(LLM_MODEL)

    rag = RAGPipeline(retriever, reranker, llm_service)

    # Ingestion components
    loader = Loader()
    cleaner = Cleaner()
    chunker = Chunker()

    ingestion = IngestionService(
        loader,
        cleaner,
        chunker,
        embedder,
        qdrant_store
    )

    print("✅ System ready!\n")

    while True:
        print("1️⃣ Upload file")
        print("2️⃣ Ask question")
        print("3️⃣ Exit")

        choice = input("> ")

        if choice == "1":
            file_path = input("📂 Nhập đường dẫn file: ")

            try:
                ingestion.ingest(file_path)
                print("✅ Ingestion xong!\n")
            except Exception as e:
                print(f"❌ Lỗi: {e}")

        elif choice == "2":
            query = input("🧠 Bạn hỏi gì?\n> ")
            print("\n🤖 Đang xử lý...\n")
            answer = rag.run(query)
            print("📌 Trả lời:\n")
            print(answer)
            print("\n" + "=" * 50 + "\n")

        elif choice == "3":
            break

        else:
            print("⚠️ Chọn lại.")


if __name__ == "__main__":
    main()