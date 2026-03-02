from typing import List
from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore
from config.settings import TOP_K


class Retriever:

    def __init__(self, embedder: Embedder, qdrant_store: QdrantStore):
        self.embedder = embedder
        self.qdrant_store = qdrant_store

    def retrieve(self, query: str, top_k: int = TOP_K) -> List[str]:

        query_vector = self.embedder.embedding_query(query)

        results = self.qdrant_store.search(query_vector, top_k)

        texts = [r.payload["text"] for r in results]

        return texts