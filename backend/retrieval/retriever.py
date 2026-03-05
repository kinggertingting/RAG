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

        dense_results = self.vector_store.search(
            query_vector,
            top_k=top_k
        )

        documents = []

        for r in dense_results:
            documents.append({
                "id": r.id,
                "text": r.payload["text"],
                "file_id": r.payload.get("file_id"),
                "file_name": r.payload.get("file_name"),
                "chunk_index": r.payload.get("chunk_index"),
                "dense_score": r.score
            })

        if self.bm25:
            self.bm25.index(documents)
            sparse_results = self.bm25.retrieve(query, top_k=top_k)

            combined = documents + sparse_results
        else:
            combined = documents

        return combined