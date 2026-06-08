import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from langfuse import observe, get_client, propagate_attributes
from app.models.schemas import HealthResponse, QueryRequest, QueryResponse, UploadResponse, SourceItem
from app.services.document_loader import load_document
from app.services.vector_store import process_and_store_document
from app.services.retrieval import retrieve_relevant_chunks
from app.services.llm import generate_answer
from app.services.session_manager import reset_session
from app.core.config import settings

router = APIRouter()

# Directory to save uploaded documents
UPLOAD_DIRECTORY = settings.UPLOAD_DIR
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Valid extensions for document upload
VALID_EXTENSIONS = {".pdf", ".docx"}

@router.get("/health", response_model=HealthResponse, tags=["status"])
async def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return HealthResponse(status="ok")

@router.post("/reset", tags=["session"])
async def reset():
    """
    Reset the session by clearing uploaded documents and the vector database.
    """
    try:
        reset_session()
        return {"message": "Session reset successful"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reset session: {str(e)}"
        )

@router.post("/upload", response_model=UploadResponse, tags=["rag"])
async def upload_document(file: UploadFile = File(...), reset: bool = False):
    """
    Endpoint for uploading PDF and DOCX documents.
    Validates file type, saves locally, and extracts text.
    If reset=True, it clears previous data before processing the new file.
    """
    # 0. Check for session reset
    if reset:
        reset_session()

    # 1. Validate file extension
    ext = os.path.splitext(file.filename)[-1].lower()
    if ext not in VALID_EXTENSIONS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type: {ext}. Only PDF and DOCX are allowed."
        )

    # 2. Save the file locally
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Could not save file: {str(e)}"
        )

    # 3. Extract text using document loader service
    extracted_text = load_document(file_path)

    # 4. Validate extraction (ensure it's not a scanned image or empty)
    if len(extracted_text) < 10:
        raise HTTPException(
            status_code=400,
            detail=(
                "The extracted text is too short. This often happens with scanned/image-based PDFs. "
                "Please upload a text-based PDF or use an OCR tool."
            )
        )

    # 5. Process text and store in ChromaDB
    num_chunks = process_and_store_document(extracted_text, file.filename)

    return UploadResponse(
        message="File uploaded, processed, and indexed successfully",
        filename=file.filename,
        extracted_text_length=len(extracted_text),
        num_chunks=num_chunks,
        status="success"
    )

@observe(name="rag-query")
async def process_rag_query(query: str, top_k: int):
    with propagate_attributes(
        metadata={"query": query, "top_k": str(top_k)},
        tags=["rag", "query"],
    ):
        retrieved_data = retrieve_relevant_chunks(query, top_k=top_k)
        context_texts = [item["text"] for item in retrieved_data]
        answer = generate_answer(query, context_texts)

        sources = [
            SourceItem(
                filename=item["filename"],
                snippet=f"{item['text'][:200]}..." if len(item["text"]) > 200 else item["text"]
            )
            for item in retrieved_data[:3]
        ]

        lf = get_client()
        lf.update_current_span(
            input={"query": query},
            output={"answer": answer, "num_chunks_used": len(retrieved_data)},
        )

    return answer, retrieved_data, sources


@router.post("/query", response_model=QueryResponse, tags=["rag"])
async def query_rag(query_data: QueryRequest):
    print("test1")
    answer, retrieved_data, sources = await process_rag_query(
        query_data.query, query_data.top_k
    )
    return QueryResponse(
        query=query_data.query,
        answer=answer,
        num_chunks_used=len(retrieved_data),
        sources=sources
    )

