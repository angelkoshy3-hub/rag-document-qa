from typing import List
from langchain_chroma import Chroma  # fix the deprecation warning too
from langchain_openai import OpenAIEmbeddings
from langfuse import observe, get_client
from app.core.config import settings
from fastapi import HTTPException

VECTOR_DB_DIR = settings.VECTOR_DB_DIR

@observe(name="retrieval")
def retrieve_relevant_chunks(query: str, top_k: int = 3) -> List[str]:
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY
        )

        vector_store = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=embeddings,
            collection_name="rag_collection"
        )

        results = vector_store.similarity_search(query, k=top_k)
        filenames = list(set(doc.metadata.get("filename", "Unknown") for doc in results))

        # ✅ correct v4 method
        lf = get_client()
        print("test6")
        lf.update_current_span(
            input={"query": query, "top_k": top_k},
            output={"num_chunks": len(results), "filenames": filenames},
            metadata={
                "vector_db": "ChromaDB",
                "collection": "rag_collection",
                "embedding_model": "text-embedding-3-small",
            },
        )

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


