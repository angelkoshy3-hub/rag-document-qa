# 🚀 RAG-Based Document Q&A System

A production-style **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based on their content. The system uses semantic search to retrieve relevant context and generates accurate answers using OpenAI models.

---

## 📌 Features

* 📄 Upload PDF documents
* ✂️ Automatic text chunking
* 🧠 Semantic search using vector embeddings
* 🔍 Context retrieval using ChromaDB
* 🤖 AI-powered answers using OpenAI
* ⚡ FastAPI-based REST APIs
* 💬 Simple chat interface
* 📚 Source-aware responses
* 📈 Langfuse observability and tracing
* 🐳 Dockerized deployment
* ☸️ Kubernetes deployment support

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Uvicorn

### AI & Retrieval

* OpenAI API
* LangChain
* ChromaDB
* OpenAI Embeddings

### Observability

* Langfuse

### Deployment

* Docker
* Kubernetes

### Frontend

* HTML
* CSS

---

## 🏗️ Architecture

```text
User Query
    ↓
FastAPI Application
    ↓
Retriever (ChromaDB)
    ↓
Relevant Context Chunks
    ↓
OpenAI LLM
    ↓
Generated Answer
    ↓
Langfuse Monitoring & Tracing
```

---

## 📂 Project Structure

```text
app/
├── api/
├── core/
├── models/
├── services/
└── main.py

data/
├── raw_docs/
└── vector_db/

Dockerfile
k8s-manifest.yaml
requirements.txt
README.md
```

---

## ⚙️ Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/angelkoshy3-hub/rag-document-qa.git
cd rag-document-qa
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

### 5. Run Application

```bash
python -m uvicorn app.main:app --reload
```

### 6. Open in Browser

```text
http://127.0.0.1:8000
```

---

## 📊 How It Works

1. User uploads a PDF document.
2. Text is extracted from the document.
3. Content is split into smaller chunks.
4. Chunks are converted into vector embeddings.
5. Embeddings are stored in ChromaDB.
6. User submits a question.
7. Relevant chunks are retrieved using semantic search.
8. OpenAI generates an answer using retrieved context.
9. Requests and responses are tracked through Langfuse.

---

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t rag-project .
```

### Run Container

```bash
docker run -p 8000:8000 rag-project
```

### Access Application

```text
http://localhost:8000
```

---

## ☸️ Kubernetes Deployment

### Load Docker Image into Minikube

```bash
minikube image load rag-project
```

### Apply Kubernetes Manifest

```bash
kubectl apply -f k8s-manifest.yaml
```

### Verify Resources

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

### Port Forward Service

```bash
kubectl port-forward service/rag-app-service 8000:8000
```

### Access Application

```text
http://localhost:8000
```

---

## 📈 Langfuse Monitoring

The project integrates Langfuse for LLM observability.

Features include:

* Prompt tracing
* Response tracking
* Request monitoring
* Debugging AI interactions
* Evaluation and analytics

This helps monitor and analyze LLM performance in production environments.

---

## 🔥 Future Improvements

* Multi-user document support
* Authentication and authorization
* Persistent vector database storage
* CI/CD pipeline
* Cloud deployment (AWS/GCP/Azure)
* Horizontal scaling with Kubernetes
* Streaming LLM responses
* Advanced RAG evaluation metrics

---

## 👩‍💻 Author

Angel Aniyan

Python Backend Developer | AI Enthusiast | AI Engineering Learner
