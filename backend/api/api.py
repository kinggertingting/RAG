from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from fastapi.middleware.cors import CORSMiddleware

# Ingestion
from ingestion.loader import Loader
from ingestion.cleaner import Cleaner
from ingestion.chunker import Chunker
from ingestion.embedder import Embedder
from ingestion.ingestion_service import IngestionService

from vector_store.qdrant_store import QdrantStore

from retrieval.retriever import Retriever
from rerank.cross_encoder import CrossEncoderModel
from rerank.rerank import Reranker

from llm.llm_service import LLMService

from rag.rag_pipeline import RAGPipeline

from config.settings import (
    QDRANT_HOST,
    QDRANT_PORT,
    LLM_MODEL,
    RERANK_MODEL
)

from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loader = Loader()
cleaner = Cleaner()
chunker = Chunker()
embedder = Embedder("")

vector_store = QdrantStore(QDRANT_HOST, QDRANT_PORT)

retriever = Retriever(embedder, vector_store)

cross_encoder = CrossEncoderModel(RERANK_MODEL)
reranker = Reranker(cross_encoder)

llm = LLMService(LLM_MODEL)

ingestion_service = IngestionService(
    loader,
    cleaner,
    chunker,
    embedder,
    vector_store
)

rag_pipeline = RAGPipeline(
    retriever=retriever,
    reranker=reranker,
    llm_service=llm
)

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
def init_qdrant():
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    collection_name = "rag-collection"

    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

@app.get("/get_all_files")
def list_files():
    return {"files": vector_store.list_files()}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        result = ingestion_service.ingest(file)

        return {
            "message": "Upload & Ingestion successful",
            "file_id": result["file_id"],
            "chunks": result["num_chunks"]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/query")
async def query(req: QueryRequest):
    try:
        result = rag_pipeline.run(req.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/check_size_file")
async def check_size_file(files: List[UploadFile] = File(...)):
    try:
        for f in files:
            loader.check_max_size_file(f)

        return JSONResponse(content={
            "message": "Size sum all of files is valid"
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/check_content_file")
async def check_content_file(file: UploadFile = File(...)):
    try:

        file_hash = loader.hash_content_file(file)
        file.file.seek(0)

        exists = vector_store.check_content_file_exists(file_hash)

        return {"exists": exists}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/delete_qdrant/{file_id}")
async def delete_qdrant(file_id: str):
    try:
        vector_store.delete_by_file_id(file_id)

        return JSONResponse(content={
            "message": "Qdrant file deleted successfully"
        })

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.delete("/delete_all_files")
async def delete_all_files():
    try:
        vector_store.delete_by_source()

        return {"message": "All files deleted"}

    except Exception as e:
        raise HTTPException(500, str(e))    