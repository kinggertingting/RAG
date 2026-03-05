from rank_bm25 import BM25Okapi
import numpy as np

class BM25Retriever:

    def __init__(self):
        self.documents = []
        self.bm25 = None

    def index(self, documents):
        self.documents = documents
        tokenized = [doc["text"].split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query, top_k=5):
        tokenized_query = query.split()
        scores = self.bm25.get_scores(tokenized_query)

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            doc = self.documents[idx]
            doc["bm25_score"] = float(scores[idx])
            results.append(doc)

        return results