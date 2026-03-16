import sys
import os

os.environ["OPENAI_API_KEY"] = "dummy"

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from datasets import Dataset
from tqdm import tqdm

from ragas import evaluate
from ragas.metrics import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)

from openai import OpenAI
from ragas.llms import llm_factory

from langchain_community.embeddings import HuggingFaceEmbeddings

from rag.rag_pipeline import RAGPipeline
from retrieval.retriever import Retriever
from rerank.rerank import Reranker
from llm.llm_service import LLMService


def load_dataset(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_pipeline(pipeline, dataset):

    questions = []
    answers = []
    contexts = []
    ground_truths = []

    for item in tqdm(dataset, desc="Running RAG pipeline"):

        question = item["question"]
        ground_truth = item["ground_truth"]

        result = pipeline.run(question)

        context_texts = [
            f"[Document {i+1}] {doc['text']}"
                 for i, doc in enumerate(result.get("contexts", [])[:3])
            ]

        questions.append(question)
        answers.append(result.get("answer", ""))
        contexts.append(context_texts)
        ground_truths.append(ground_truth)

    return Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })



def main():

    print("\nLoading evaluation dataset...")

    dataset = load_dataset("evaluation/eval_dataset.json")

    print("Initializing RAG pipeline...")

    pipeline = RAGPipeline(
        Retriever(),
        Reranker(),
        LLMService()
    )

    rag_dataset = run_pipeline(pipeline, dataset)

    print("\nInitializing evaluator LLM (llama.cpp)...")

    client = OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="dummy"
    )

    evaluator_llm = llm_factory(
        "qwen2.5-1.5b-q4.gguf",
        client=client
    )

    print("Loading embedding model for RAGAS...")

    embeddings = HuggingFaceEmbeddings(
        model_name="intfloat/multilingual-e5-small"
    )

    print("\nRunning RAG evaluation...")

    results = evaluate(
        rag_dataset,
        metrics=[
            Faithfulness(),
            AnswerRelevancy(),
            ContextPrecision(),
            ContextRecall()
        ],
        llm=evaluator_llm,
        embeddings=embeddings
    )

    print("\n===== RAG Evaluation Results =====")
    print(results)


if __name__ == "__main__":
    main()