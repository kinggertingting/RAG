from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore
from config.settings import TOP_K
from retrieval.bm25_retriever import BM25Retriever


class Retriever:

    def __init__(self, embedder=Embedder(), vector_store=QdrantStore(), bm25=BM25Retriever()):
        self.embedder = embedder
        self.vector_store = vector_store
        self.bm25 = bm25

    def retrieve(self, query, top_k=TOP_K):

        query_vector = self.embedder.embedding_query(query)

        dense_results = self.vector_store.search(query_vector, top_k)

        sparse_results = self.bm25.retrieve(query, top_k)

        combined = dense_results + sparse_results

        unique = {}
        for doc in combined:
            key = (doc["file_id"], doc["chunk_index"])
            if key not in unique:
                unique[key] = doc

        return list(unique.values())