from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter, FieldCondition, MatchValue
)
from config.settings import COLLECTION_NAME, VECTOR_DIM, QDRANT_HOST, QDRANT_PORT, TOP_K
import uuid

class QdrantStore:

    def __init__(self, host: str = QDRANT_HOST, port: int = QDRANT_PORT):
        self.client = QdrantClient(host=host , port=port )
        self.collection_name = COLLECTION_NAME

        self._create_collection_if_not_exists()

    # Create collection
    def _create_collection_if_not_exists(self):

        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=VECTOR_DIM,
                    distance=Distance.COSINE
                )
            )

    # Insert vectors (Ingestion)
    def insert(self, embeddings, chunks, filename: str):

        points = []

        for vector, text in zip(embeddings, chunks):
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector.tolist(),
                    payload={
                        "text": text,
                        "source": filename
                    }
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def delete_by_source(self, filename: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="source",
                        match=MatchValue(value=filename)
                    )
                ]
            )
        )

    # Search vectors (Query time)
    def search(self, query_vector, top_k: int = TOP_K):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=top_k
        )
        # print("Results:", results)
        # print("Type of first result:", type(results[0]))
        return results.points