"""
API schemas.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractRequest(BaseModel):
    """Extract from URLs."""
    urls: List[str] = Field(..., min_items=1, max_items=10)
    model: Optional[str] = None


class SearchRequest(BaseModel):
    """Search and extract."""
    query: str = Field(..., min_length=3)
    max_urls: int = Field(default=3, ge=1, le=10)
    model: Optional[str] = None


class ExtractResponse(BaseModel):
    """Extraction response."""
    urls_processed: int
    urls: List[str] = []
    summary: str
    model_used: str
    processing_time: float


class HealthResponse(BaseModel):
    """Health check."""
    status: str = "healthy"
    version: str
