


## 🚀 RAG-Based Document Q&A System

A production-style **Retrieval-Augmented Generation (RAG)** backend system that allows users to upload documents and ask questions based on their content.

---

## 📌 Features

* 📄 Upload PDF documents
* ✂️ Automatic text chunking
* 🧠 Semantic search using vector embeddings
* 🔍 Context retrieval using ChromaDB
* 🤖 AI-powered answers using OpenAI API
* ⚡ FastAPI-based REST APIs
* 💬 Simple UI with chat interface
* 📚 Source-based answers (context chunks)

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI
* **LLM Integration:** OpenAI API
* **Framework:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** OpenAI Embeddings
* **Frontend:** HTML, CSS
* **Others:** Uvicorn

---

## 🏗️ Architecture

```text
User Query
   ↓
Retriever (ChromaDB)
   ↓
Relevant Chunks
   ↓
LLM (OpenAI)
   ↓
Final Answer
```

---

## ⚙️ Setup Instructions

### 1. Clone repo

```bash
git clone https://github.com/angelkoshy3-hub/rag-document-qa.git
cd rag-document-qa
```

---

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Add environment variables

Create `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

---

### 5. Run the server

```bash
python -m uvicorn app.main:app --reload
```

---

### 6. Open in browser

```
http://127.0.0.1:8000
```

---

## 📊 How it Works

1. Upload a document (PDF)
2. Text is extracted and split into chunks
3. Chunks are converted into embeddings
4. Stored in ChromaDB
5. User asks a question
6. Relevant chunks are retrieved
7. LLM generates answer using context

---

## 📂 Project Structure

```text
app/
 ├── api/
 ├── core/
 ├── services/
 ├── models/
 └── main.py

data/
 ├── raw_docs/
 └── vector_db/
```

---

## 🔥 Future Improvements

* Multi-user support
* Session-based document isolation
* Authentication system
* Streaming responses
* Better UI (React)

---

## 👩‍💻 Author

**Angel Aniyan**
Python Backend Developer | AI Enthusiast

---
