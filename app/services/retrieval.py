from typing import List
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from fastapi import HTTPException

# Directory where the vector store is persisted
VECTOR_DB_DIR = settings.VECTOR_DB_DIR

def retrieve_relevant_chunks(query: str, top_k: int = 3) -> List[str]:
    """
    Retrieve the most relevant document chunks from ChromaDB based on the query.
    """
    try:
        # 1. Initialize embeddings (must match the model used for storage)
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # 2. Load the existing vector store
        vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="rag_collection"
        )
        
        # 3. Perform similarity search
        results = vector_store.similarity_search(query, k=top_k)
        
        # 4. Extract and return content with metadata
        return [
            {
                "text": doc.page_content,
                "filename": doc.metadata.get("filename", "Unknown")
            }
            for doc in results
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving relevant chunks: {str(e)}"
        )
