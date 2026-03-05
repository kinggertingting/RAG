
import time

from ingestion.loader import Loader
from ingestion.cleaner import Cleaner
from ingestion.chunker import Chunker
from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore
import uuid

class IngestionService:

    def __init__(self, loader, cleaner, chunker, embedder, qdrant):
        self.loader = loader or Loader()
        self.cleaner = cleaner or Cleaner()
        self.chunker = chunker or Chunker()
        self.embedder = embedder or Embedder()
        self.qdrant = qdrant or QdrantStore(host=None, port=None)

    def ingest(self, file):

        file_id = str(uuid.uuid4())

        file_hash = self.loader.hash_content_file(file)
        file.file.seek(0)

        if self.qdrant.check_content_file_exists(file_hash):
            raise ValueError("Content file is already ingested")

        text = self.loader.load_file(file)

        if not text.strip():
            raise ValueError("File is empty")

        text = self.cleaner.clean_text(text)

        chunks = self.chunker.chunking(text)

        if not chunks:
            raise ValueError("No chunk created")

        embeddings = self.embedder.embedding_passages(chunks)

        payloads = [
        {
            "text": chunk,
            "file_id": file_id,
            "file_name": file.filename,
            "file_hash": file_hash,
            "chunk_index": i,
            "source": "upload",
            "timestamp": time.time()
        }
        for i, chunk in enumerate(chunks)
    ]

        self.qdrant.insert(embeddings, payloads, file_id, file_hash)

        return {
            "file_id": file_id,
            "num_chunks": len(chunks),
            "vector_dim": embeddings.shape[1]
    }