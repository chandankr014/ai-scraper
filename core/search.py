"""
Google Custom Search API based search module.

Provides robust URL retrieval using Google's Custom Search JSON API
with proper error handling, retry logic, and rate limiting.
"""

from typing import List, Optional, Union
import os
import time
import requests
from urllib.parse import quote_plus
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logger import get_logger
logger = get_logger(__name__)


# Custom Exceptions
class SearchError(Exception):
    """Base exception for search-related errors."""
    pass


class RateLimitError(SearchError):
    """Raised when the API rate limit is exceeded."""
    pass


class APIQuotaExceededError(SearchError):
    """Raised when the daily API quota is exceeded."""
    pass


# API Configuration
GOOGLE_SEARCH_API_URL = "https://www.googleapis.com/customsearch/v1"
SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY", "")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
RETRY_DELAY_BASE = float(os.getenv("RETRY_DELAY_BASE", "1.0"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))


def _make_search_request(query: str, num_results: int = 10, start_index: int = 1) -> dict:
    """
    Make a single search request to Google Custom Search API.
    
    Args:
        query: Search query string
        num_results: Number of results to return (max 10 per request)
        start_index: Starting index for pagination
    
    Returns:
        JSON response from the API
    
    Raises:
        SearchError: If the request fails after retries
        RateLimitError: If rate limited by the API
        APIQuotaExceededError: If daily quota is exceeded
    """
    params = {
        "key": SEARCH_API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": min(num_results, 10),  # Google API allows max 10 per request
        "start": start_index,
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(
                GOOGLE_SEARCH_API_URL,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                return response.json()
            
            elif response.status_code == 429:
                # Rate limited
                retry_after = int(response.headers.get("Retry-After", RETRY_DELAY_BASE * (2 ** attempt)))
                logger.warning(f"Rate limited. Retrying after {retry_after}s (attempt {attempt + 1}/{MAX_RETRIES})")
                time.sleep(retry_after)
                continue
            
            elif response.status_code == 403:
                error_data = response.json()
                error_reason = error_data.get("error", {}).get("errors", [{}])[0].get("reason", "")
                
                if "dailyLimitExceeded" in error_reason or "quotaExceeded" in error_reason:
                    raise APIQuotaExceededError(f"Google Search API quota exceeded: {error_reason}")
                elif "rateLimitExceeded" in error_reason:
                    raise RateLimitError(f"Rate limit exceeded: {error_reason}")
                else:
                    raise SearchError(f"API access forbidden: {response.text}")
            
            elif response.status_code == 400:
                error_data = response.json()
                raise SearchError(f"Bad request: {error_data.get('error', {}).get('message', response.text)}")
            
            else:
                logger.warning(f"Search request failed with status {response.status_code} (attempt {attempt + 1}/{MAX_RETRIES})")
                if attempt < MAX_RETRIES - 1:
                    delay = RETRY_DELAY_BASE * (2 ** attempt)
                    time.sleep(delay)
                    continue
                raise SearchError(f"Search request failed: {response.status_code} - {response.text}")
        
        except requests.exceptions.Timeout:
            logger.warning(f"Request timeout (attempt {attempt + 1}/{MAX_RETRIES})")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_BASE * (2 ** attempt))
                continue
            raise SearchError("Search request timed out after all retries")
        
        except requests.exceptions.ConnectionError as e:
            logger.warning(f"Connection error (attempt {attempt + 1}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY_BASE * (2 ** attempt))
                continue
            raise SearchError(f"Connection error: {e}")
    
    raise SearchError("Search failed after all retries")


def search(
    query: Union[str, List[str]], 
    max_results: int = 4,
    deduplicate: bool = True
) -> List[str]:
    """
    Search for URLs using Google Custom Search API.
    
    Args:
        query: Single search query string or list of query strings
        max_results: Maximum number of results per query (default: 10)
        deduplicate: Remove duplicate URLs across queries (default: True)
    
    Returns:
        List of unique URLs from search results
    
    Example:
        >>> urls = search("flood prediction machine learning")
        >>> urls = search(["flood news India", "monsoon updates 2024"], max_results=5)
    """
    # Normalize query to list
    query_list = [query] if isinstance(query, str) else query
    
    if not query_list:
        logger.warning("Empty query list provided")
        return []
    
    all_urls = []
    seen_urls = set()
    
    for q in query_list:
        if not q or not q.strip():
            logger.warning("Skipping empty query")
            continue
        
        logger.info(f"Searching for: {q}")
        
        try:
            # Calculate how many requests we need (API returns max 10 per request)
            results_to_fetch = min(max_results, 10)  # limits to 10 results total
            urls_for_query = []
            
            for start in range(1, results_to_fetch + 1, 10):
                batch_size = min(10, results_to_fetch - start + 1)
                
                try:
                    result = _make_search_request(q, num_results=batch_size, start_index=start)
                    
                    items = result.get("items", [])
                    if not items:
                        logger.debug(f"No more results for query: {q}")
                        break
                    
                    for item in items:
                        url = item.get("link", "")
                        if url:
                            if deduplicate:
                                if url not in seen_urls:
                                    seen_urls.add(url)
                                    urls_for_query.append(url)
                            else:
                                urls_for_query.append(url)
                        
                        if len(urls_for_query) >= max_results:
                            break
                    
                    if len(urls_for_query) >= max_results:
                        break
                    
                    # Small delay between pagination requests to avoid rate limiting
                    time.sleep(0.1)
                    
                except APIQuotaExceededError:
                    logger.error("API quota exceeded. Cannot continue searching.")
                    raise
                except RateLimitError as e:
                    logger.warning(f"Rate limited during pagination: {e}")
                    break
            
            logger.info(f"Found {len(urls_for_query)} URLs for query: {q}")
            all_urls.extend(urls_for_query)
            
        except SearchError as e:
            logger.error(f"Search error for query '{q}': {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error searching for '{q}': {e}")
            continue
    
    logger.info(f"Total URLs retrieved: {len(all_urls)}")
    return all_urls


def search_single(query: str, max_results: int = 10) -> List[str]:
    """
    Convenience function for searching a single query.
    
    Args:
        query: Search query string
        max_results: Maximum number of results (default: 10)
    
    Returns:
        List of URLs from search results
    """
    return search(query, max_results=max_results)


def search_batch(queries: List[str], max_results_per_query: int = 4) -> List[str]:
    """
    Search multiple queries and return combined, deduplicated results.
    
    Args:
        queries: List of search query strings
        max_results_per_query: Maximum results per query (default: 5)
    
    Returns:
        List of unique URLs from all queries
    """
    return search(queries, max_results=max_results_per_query, deduplicate=True)

