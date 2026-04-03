from pydantic import BaseModel
from typing import List, Optional

class HealthResponse(BaseModel):
    """Schema for health check response"""
    status: str = "ok"

class QueryRequest(BaseModel):
    """Schema for incoming RAG queries"""
    query: str
    top_k: Optional[int] = 3

class SourceItem(BaseModel):
    """Schema for a single document source reference"""
    filename: str
    snippet: str

class QueryResponse(BaseModel):
    """Schema for RAG query results"""
    query: str
    answer: str
    num_chunks_used: int
    sources: Optional[List[SourceItem]] = []

class UploadResponse(BaseModel):
    """Schema for successful document upload"""
    message: str
    filename: str
    extracted_text_length: int
    num_chunks: int
    status: str = "success"
