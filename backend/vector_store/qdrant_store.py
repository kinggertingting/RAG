from qdrant_client import QdrantClient
from qdrant_client.models import (
    FilterSelector,
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


    def list_files(self):

        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=1000,
            with_payload=True
        )

        files = {}

        for point in results:
            payload = point.payload

            file_id = payload.get("file_id")
            file_name = payload.get("file_name")

            if file_id not in files:
                files[file_id] = {
                    "file_id": file_id,
                    "file_name": file_name
                }

        return list(files.values())

    # Insert vectors (Ingestion)
    def insert(self, embeddings, payloads, file_id: str, file_hash: str):
        points = []

        for vector, payload in zip(embeddings, payloads):

            payload["file_id"] = file_id
            payload["file_hash"] = file_hash

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector.tolist(),
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

    def check_content_file_exists(self, file_hash: str) -> bool:

        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            scroll_filter={
                "must": [
                    {
                        "key": "file_hash",
                        "match": {"value": file_hash}
                    }
                ]
            },
            limit=1
        )

        return len(results) > 0


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

    def delete_by_file_id(self, file_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=FilterSelector(
                filter=Filter(
                    must=[
                        FieldCondition(
                            key="file_id",
                            match=MatchValue(value=file_id)
                        )
                    ]
                )
            )
        )

    # Search vectors (Query time)
    def search(self, query_vector, top_k: int = TOP_K):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector.tolist(),
            limit=top_k
        )

        docs = []

        for point in results.points:

            payload = point.payload.copy()

            payload["score"] = point.score

            docs.append(payload)

        return docs