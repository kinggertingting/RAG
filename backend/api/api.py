from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from ingestion.loader import Loader
from ingestion.cleaner import Cleaner
from ingestion.chunker import Chunker
from ingestion.embedder import Embedder
from vector_store.qdrant_store import QdrantStore
from retrieval.retriever import Retriever
from llm.llm_service import LLMService

from config.settings import QDRANT_HOST, QDRANT_PORT, LLM_MODEL

app = FastAPI()

# ===== INIT SERVICES =====
loader = Loader()
cleaner = Cleaner()
chunker = Chunker()
embedder = Embedder("")
vector_store = QdrantStore(QDRANT_HOST, QDRANT_PORT)
retriever = Retriever(embedder, vector_store)
llm = LLMService(LLM_MODEL)


# ==============================
# 📂 UPLOAD & INGEST
# ==============================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # 1. Load
        raw_text = loader.load_file(file)

        # 2. Clean
        clean_text = cleaner.clean_text(raw_text)

        # 3. Chunk
        chunks = chunker.chunking(clean_text)

        # 4. Embed
        embeddings = embedder.embedding_passages(chunks)

        # 5. Save to Qdrant
        vector_store.insert(embeddings, chunks, file.filename)

        return JSONResponse(
            content={
                "message": "Upload & Ingestion thành công",
                "chunks": len(chunks)
            }
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ==============================
# 💬 QUERY
# ==============================
@app.post("/query")
async def query(question: str):
    try:
        # 1. Retrieve
        results = retriever.retrieve(question)

        context = "\n\n".join(results)

        # 2. Prompt
        prompt = f"""
        Bạn là trợ lý AI chuyên trả lời dựa trên tài liệu được cung cấp.

        QUY TẮC:
        - Chỉ được trả lời dựa trên thông tin trong ngữ cảnh.
        - Nếu ngữ cảnh không chứa thông tin để trả lời, hãy nói:
        "Tôi không tìm thấy thông tin trong tài liệu."
        - Không được tự suy đoán hoặc sử dụng kiến thức bên ngoài.

        {context}

        Câu hỏi: {question}
        """

        # 3. Generate
        answer = llm.generate_response(prompt)

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))