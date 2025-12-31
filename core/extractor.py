"""
Extract key information from content using LLM.
"""
from typing import List, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.llm_client import chat
from utils.logger import get_logger

logger = get_logger(__name__)

EXTRACTION_PROMPT = """Extract key information from the content below.

Provide:
1. A brief summary (2-3 sentences)
2. Key facts and findings (bullet points)
3. Any relevant locations, dates, or numbers mentioned

Be concise and factual."""


def extract_from_content(content: str, model: str = None) -> str:
    """Extract key information from text content."""
    logger.info(f"Extracting from {len(content)} chars")
    
    if len(content) > 12000:
        content = content[:12000] + "\n[truncated]"
    
    try:
        result = chat(
            prompt=f"Content to analyze:\n\n{content}",
            system_prompt=EXTRACTION_PROMPT,
            model=model
        )
        logger.info("Extraction complete")
        return result
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return f"Error: {str(e)}"


def extract_from_urls(scraped_data: List[Dict], model: str = None) -> str:
    """Extract information from multiple scraped pages."""
    if not scraped_data:
        return "No content to analyze"
    
    combined = ""
    for i, item in enumerate(scraped_data, 1):
        url = item.get("url", "")
        content = item.get("content", "")
        if content:
            combined += f"\n\n=== SOURCE {i}: {url} ===\n{content[:4000]}"
    
    if not combined:
        return "No content extracted from URLs"
    
    return extract_from_content(combined, model)
