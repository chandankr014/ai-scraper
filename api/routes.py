"""
API routes.
"""
import time
import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import ExtractRequest, SearchRequest, ExtractResponse, HealthResponse
from core.scraper import scrape_urls
from core.extractor import extract_from_urls
from core.search import search
from config import API_VERSION, DEFAULT_GROQ_MODEL, LLM_PROVIDER, DEFAULT_OPENROUTER_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()

ANSWERS_DIR = Path(__file__).parent.parent / "answers"
ANSWERS_DIR.mkdir(exist_ok=True)


def get_default_model():
    return DEFAULT_GROQ_MODEL if LLM_PROVIDER == "groq" else DEFAULT_OPENROUTER_MODEL


def save_result(data: dict, prefix: str = "result"):
    """Save result to JSON file."""
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{prefix}.json"
    with open(ANSWERS_DIR / filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@router.get("/health", response_model=HealthResponse)
async def health():
    """Health check."""
    return HealthResponse(status="healthy", version=API_VERSION)


@router.post("/extract", response_model=ExtractResponse)
async def extract(request: ExtractRequest):
    """Extract information from provided URLs."""
    start_time = time.time()
    logger.info(f"Extract: {len(request.urls)} URLs")
    
    try:
        scraped = await scrape_urls(request.urls)
        model = request.model or get_default_model()
        summary = extract_from_urls(scraped, model)
        processing_time = round(time.time() - start_time, 2)
        
        save_result({
            "type": "extract",
            "urls": request.urls,
            "summary": summary,
            "model": model,
            "time": processing_time
        }, "extract")
        
        return ExtractResponse(
            urls_processed=len(scraped),
            urls=request.urls,
            summary=summary,
            model_used=model,
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search", response_model=ExtractResponse)
async def search_and_extract(request: SearchRequest):
    """Search web for query, scrape results, and extract information."""
    start_time = time.time()
    logger.info(f"Search: {request.query}")
    
    try:
        # Search for URLs
        urls = search(request.query, request.max_urls)
        if not urls:
            return ExtractResponse(
                urls_processed=0,
                urls=[],
                summary="No search results found",
                model_used=request.model or get_default_model(),
                processing_time=round(time.time() - start_time, 2)
            )
        
        # Scrape and extract
        scraped = await scrape_urls(urls)
        model = request.model or get_default_model()
        summary = extract_from_urls(scraped, model)
        processing_time = round(time.time() - start_time, 2)
        
        save_result({
            "type": "search",
            "query": request.query,
            "urls": urls,
            "summary": summary,
            "model": model,
            "time": processing_time
        }, "search")
        
        return ExtractResponse(
            urls_processed=len(scraped),
            urls=urls,
            summary=summary,
            model_used=model,
            processing_time=processing_time
        )
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
