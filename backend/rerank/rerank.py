from typing import List, Dict
from rerank.cross_encoder import CrossEncoderModel
from config.settings import RERANK_TOP_N


class Reranker:

    def __init__(self, cross_encoder: CrossEncoderModel = None):
        self.cross_encoder = cross_encoder or CrossEncoderModel()

    def rerank(self, query: str, documents: List[Dict], top_n: int = RERANK_TOP_N):

        texts = [doc["text"] for doc in documents]

        scores = self.cross_encoder.predict(query, texts)

        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)

        documents.sort(key=lambda x: x["rerank_score"], reverse=True)

        return documents[:top_n]