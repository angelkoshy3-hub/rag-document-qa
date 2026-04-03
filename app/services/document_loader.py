import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from fastapi import HTTPException

def load_document(file_path: str) -> str:
    """
    Load a document and extract its text content using LangChain loaders.
    Supports .pdf and .docx files.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    
    try:
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext == ".docx":
            loader = Docx2txtLoader(file_path)
        else:
            # This should have been caught by the API layer, but safety first
            raise HTTPException(status_code=400, detail=f"Unsupported file extension: {ext}")
        
        # Load the document and combine all pages/content into one string
        docs = loader.load()
        extracted_text = "\n".join([doc.page_content for doc in docs]).strip()
        
        return extracted_text
        
    except Exception as e:
        # Log error or handle specific loader exceptions as needed
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to read or process file: {str(e)}"
        )
