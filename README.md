# 🚀 RAG PRIVATE
### Private Retrieval-Augmented Generation Agentic System

A **Private RAG Agentic (Retrieval-Augmented Generation Agentic)** system that allows users to **upload documents and query knowledge from them using a local LLM**, without relying on external APIs.

This project focuses on building a **fully local AI system** where all data and processing stay **private and secure**.

---

# 📖 Overview

The system allows users to:

- Upload documents
- Automatically split documents into chunks
- Store embeddings in a vector database
- Retrieve relevant context when users ask questions
- Generate answers using a local LLM

The goal of this project is to demonstrate a **complete RAG pipeline**, from **document ingestion to AI-generated answers**.

---

# 🏗 Architecture

The system follows a typical **RAG pipeline architecture**:
![alt text](RAG_AGENTIC_PRIVATE_ARCHITECTURE.png)

# ⚙️ Technologies Used

This project combines several modern AI and web technologies to build a **fully local Retrieval-Augmented Generation (RAG) system**.

### 🧠 AI / Machine Learning

- **LLM:** : use llama.cpp () 
- **Inference Engine:** :contentReference[oaicite:1]{index=1} for running the LLM locally  
- **Embeddings:** :contentReference[oaicite:2]{index=2} for semantic search  

---

### 🔎 Retrieval System

- **Vector Database:** :contentReference[oaicite:3]{index=3}  
- **RAG Pipeline:** document chunking → embedding → retrieval → reranking → generation  

---

### 🖥 Backend

- **Language:** :contentReference[oaicite:4]{index=4}  
- **API Framework:** :contentReference[oaicite:5]{index=5}  
- **LLM API Interface:** :contentReference[oaicite:6]{index=6} compatible endpoint  

---

### 🌐 Frontend

- **Framework:** :contentReference[oaicite:7]{index=7}  
- **Language:** :contentReference[oaicite:8]{index=8}  
- **Styling:** :contentReference[oaicite:9]{index=9}  

---

### 🐳 Infrastructure

- **Containerization:** :contentReference[oaicite:10]{index=10}  
- **Orchestration:** :contentReference[oaicite:11]{index=11}  

---

### 📦 Model & Dataset Hosting

- **Model Hub:** :contentReference[oaicite:12]{index=12}

---

# 🧭 How to Use Application "Private RAG Agentic"

### 1 Upload Documents

Users upload documents through the web interface.

The backend will automatically:

- Extract text from the document
- Split the text into chunks
- Generate embeddings
- Store vectors in the vector database

### 2 Ask Questions

Users can ask questions in the chat interface.

The system will:

1. Convert the question into embeddings
2. Retrieve relevant chunks from the vector database
3. Rerank the retrieved results
4. Send the context to the LLM
5. Generate the final answer

---

### 3 View Sources

The system also returns **source snippets** so users can see where the answer came from.

---



### How to implement this project

# 1. Download the project

First, download the project to your local machine.

You can do this in two ways:

### Option 1 — Clone the repository (recommended)

```bash
git clone <your-repository-url>
```

Then move into the project directory:

```bash
cd RAG_PRIVATE
```

### Option 2 — Download ZIP

1. Go to the GitHub repository
2. Click **Code → Download ZIP**
3. Extract the ZIP file to your computer
4. Open a terminal in the extracted folder

---

# 2. Download the LLaMA model

Open CLI (Command Line at source project)

This project uses the **Qwen2.5 1.5B Q4 quantized model**.

First, open a terminal in the root project directory and run:

```bash
huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF \
  qwen2.5-1.5b-instruct-q4_k_m.gguf \
  --local-dir ./models
```

After downloading, the model will be stored in:

```
./models/qwen2.5-1.5b-instruct-q4_k_m.gguf
```

Example project structure:

```
RAG_PRIVATE
│
├── backend
├── frontend
├── models
│   └── qwen2.5-1.5b-instruct-q4_k_m.gguf
├── docker-compose.yml
└── README.md
```

This model will be loaded by the **llama.cpp server** when the backend starts.

# 3. Start the system with Docker

Make sure you have installed:

- Docker
- Docker Compose

Then run:

```bash
docker compose up --build
```

Docker will start multiple services including:

- Backend API
- LLM server
- Vector database
- Frontend application

---

# 4. Access the application

Once the containers are running, open your browser and go to:

```
http://localhost:3000
```

You should now see the **Private RAG interface**.

---

# 5. Upload documents

Upload documents such as:

- PDF
- TXT
- DOCX

The system will automatically:

1. Extract text
2. Split text into chunks
3. Generate embeddings
4. Store them in the vector database

---

# 6. Ask questions

After uploading documents, you can ask questions in the chat interface.

The system will:

1. Convert the question into embeddings
2. Retrieve relevant chunks
3. Rerank the results
4. Send the context to the LLM
5. Generate the final answer

# 7. The api to test all function

Backend: Uvicorn (http://localhost:8000) (You can wait a few minutes to backend start)

Frontend: (http://localhost:3000)

Qdrant: (http://localhost:6333)



