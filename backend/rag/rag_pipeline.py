from typing import List
from retrieval.retriever import Retriever
from rerank.rerank import Reranker
from llm.llm_service import LLMService
from config.settings import TOP_K, RERANK_TOP_N


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
        return "\n\n".join(doc["text"] for doc in documents)

    def run(self, query: str) -> str:

        retrieved_docs = self.retriever.retrieve(query, top_k=TOP_K)

        if not retrieved_docs:
            return "Không tìm thấy thông tin liên quan."

        if isinstance(retrieved_docs[0], str):
            retrieved_docs = [{"text": t} for t in retrieved_docs]

        reranked_docs = self.reranker.rerank(
            query,
            retrieved_docs,
            top_n=RERANK_TOP_N
        )

        context = self._build_context(reranked_docs)

        answer = self.llm_service.generate_response(
            query=query,
            context=context
        )

        return answer