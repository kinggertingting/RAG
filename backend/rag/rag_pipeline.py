import time
from typing import List
from retrieval.retriever import Retriever
from rerank.rerank import Reranker
from llm.llm_service import LLMService
from config.settings import SCORE_THRESHOLD, TOP_K, RERANK_TOP_N


class RAGPipeline:

    def __init__(
        self,
        retriever: Retriever,
        reranker: Reranker,
        llm_service: LLMService
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.llm_service = llm_service

    def _build_context(self, documents: List[dict]) -> str:
        context = ""

        for doc in documents:
            context += f"""
            FILE: {doc.get("file_name")}
            CHUNK: {doc.get("chunk_index")}

            {doc.get("text")}
            ---------------------
            """
        return context

    def run(self, query: str):

        start_time = time.time()

        retrieved_docs = self.retriever.retrieve(query)

        if not retrieved_docs:
            return {
                "answer": "Không tìm thấy thông tin liên quan.",
                "contexts": []
            }

        # remove duplicates
        unique_docs = {}
        for doc in retrieved_docs:
            key = (doc["file_id"], doc["chunk_index"])
            if key not in unique_docs:
                unique_docs[key] = doc

        retrieved_docs = list(unique_docs.values())

        reranked_docs = self.reranker.rerank(
            query,
            retrieved_docs,
            top_n=RERANK_TOP_N
        )

        confidence = max(doc["rerank_score"] for doc in reranked_docs)

        if confidence < SCORE_THRESHOLD:
            return {
                "answer": "Tôi không tìm thấy thông tin trong tài liệu.",
                "contexts": [],
                "confidence": confidence
            }

        context = self._build_context(reranked_docs[:3])

        answer = self.llm_service.generate_response(
            query=query,
            context=context
        )

        latency = time.time() - start_time

        return {
            "answer": answer,
            "contexts": reranked_docs,
            "confidence": confidence,
            "latency": latency
        }