import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
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

@router.post("/query", response_model=QueryResponse, tags=["rag"])
async def query_rag(query_data: QueryRequest):
    """
    Endpoint for querying the RAG system.
    Retrieves relevant context and generates a response using LLM.
    """
    # 1. Retrieve the top relevant chunks with metadata from ChromaDB
    # retrieve_relevant_chunks now returns List[dict] with 'text' and 'filename'
    retrieved_data = retrieve_relevant_chunks(query_data.query, top_k=query_data.top_k)

    # 2. Extract raw text context for the LLM
    context_texts = [item["text"] for item in retrieved_data]

    # 3. Generate an answer based on the retrieved context
    answer = generate_answer(query_data.query, context_texts)

    # 4. Prepare source attribution items (limit to top 3 sources)
    # We take a 200-character snippet from each chunk and the filename
    sources = [
        SourceItem(
            filename=item["filename"], 
            snippet=f"{item['text'][:200]}..." if len(item["text"]) > 200 else item["text"]
        )
        for item in retrieved_data[:3]
    ]

    return QueryResponse(
        query=query_data.query,
        answer=answer,
        num_chunks_used=len(retrieved_data),
        sources=sources
    )
