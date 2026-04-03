import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from app.core.config import settings
from fastapi import HTTPException

# Directory to persist the vector store
VECTOR_DB_DIR = settings.VECTOR_DB_DIR
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

# Initialize the embedding model
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=settings.OPENAI_API_KEY
)

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)

def process_and_store_document(text: str, filename: str) -> int:
    """
    Split text into chunks, generate embeddings, and store in ChromaDB.
    Returns the number of chunks processed.
    """
    try:
        # 1. Split text into chunks
        chunks = text_splitter.split_text(text)
        
        if not chunks:
            return 0
            
        # 2. Prepare metadata for each chunk
        metadatas = [{"filename": filename, "chunk_id": i} for i in range(len(chunks))]
        
        # 3. Add to ChromaDB vector store
        # We load the existing vector store or create a new one using same persist_directory
        vectorstore = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="rag_collection"
        )
        
        # Explicitly ADD texts to the existing collection (enables multi-file support)
        vectorstore.add_texts(
            texts=chunks,
            metadatas=metadatas
        )
        
        return len(chunks)
        
    except Exception as e:
        # Handle embedding or storage failures
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process or store document vectors: {str(e)}"
        )
