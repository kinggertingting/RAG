import time
from typing import List
from agent.rewrite_query import RewriteQuery
from agent.agent import Agentic
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
        self.agentic = Agentic()
        self.rewrite = RewriteQuery()

    def _build_context(self, documents: List[dict]) -> str:

        files = {}

        for doc in documents:
            file_name = doc.get("file_name", "unknown")

            if file_name not in files:
                files[file_name] = []

            files[file_name].append(doc.get("text"))

        context = ""

        for file_name, texts in files.items():

            context += f"\n===== FILE: {file_name} =====\n"

            for text in texts:
                context += text + "\n"

        return context

    def run(self, query: str):

        start_time = time.time()

        mode = self.agentic.decide(query)

        rewritten_query = self.rewrite.rewrite_query(query)

        retrieved_docs = self.retriever.retrieve(rewritten_query)

        if not retrieved_docs:
            return {
                "answer": "No relevant information found in the documents.",
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
            rewritten_query,
            retrieved_docs,
            top_n=RERANK_TOP_N
        )

        confidence = max(doc["rerank_score"] for doc in reranked_docs)

        context = self._build_context(reranked_docs[:2])

        answer = self.llm_service.generate_response(
            query=query,
            context=context,
            mode=mode
        )

        latency = time.time() - start_time

        return {
            "answer": answer,
            "contexts": reranked_docs,
            "confidence": confidence,
            "latency": latency
        }