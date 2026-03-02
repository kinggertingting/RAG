from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

class Embedder:

    def __init__(self, embedding_model: str = None):
        self.embedding_model = embedding_model or EMBEDDING_MODEL
        self.model = SentenceTransformer(self.embedding_model)

    # e5 requires prefixes
    def embedding_passages(self, chunks: List[str]) -> np.ndarray:

        chunks = ["passage: " + chunk for chunk in chunks]

        embeddings = self.model.encode(
            chunks,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )

        return embeddings


    def embedding_query(self, query: str) -> np.ndarray:

        query = "query: " + query

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding