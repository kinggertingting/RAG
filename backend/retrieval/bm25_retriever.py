from rank_bm25 import BM25Okapi
import numpy as np


class BM25Retriever:

    def __init__(self):
        self.documents = []
        self.bm25 = None

    def index(self, documents):

        if not documents:
            self.documents = []
            self.bm25 = None
            return

        self.documents = documents

        tokenized = [
            doc["text"].split()
            for doc in documents
            if doc.get("text")
        ]

        if not tokenized:
            self.bm25 = None
            return

        self.bm25 = BM25Okapi(tokenized)

    def retrieve(self, query, top_k=5):

        if self.bm25 is None or not self.documents:
            return []

        tokenized_query = query.split()

        scores = self.bm25.get_scores(tokenized_query)

        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []

        for idx in top_indices:

            doc = self.documents[idx].copy()

            doc["bm25_score"] = float(scores[idx])

            results.append(doc)

        return results