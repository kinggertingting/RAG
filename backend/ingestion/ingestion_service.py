from ingestion.loader import Loader
from ingestion.cleaner import Cleaner
from ingestion.chunker import Chunker
from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore

class IngestionService:

    def __init__(self, loader, cleaner, chunker, embedder, qdrant):
        self.loader = Loader() or loader
        self.cleaner = cleaner or Cleaner()
        self.chunker = chunker or Chunker()
        self.embedder = embedder or Embedder()
        self.qdrant = qdrant or QdrantStore(host=None, port=None)

    def ingest(self, file):

        text = self.loader.load_file(file)

        if not text.strip():
            raise ValueError("File không có nội dung")

        text = self.cleaner.clean_text(text)

        chunks = self.chunker.chunking(text)

        if not chunks:
            raise ValueError("Không tạo được chunk")

        embeddings = self.embedder.embedding_passages(chunks)

        self.qdrant.insert(embeddings, chunks)

        return {
            "num_chunks": len(chunks),
            "vector_dim": embeddings.shape[1]
        }