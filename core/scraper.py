"""
Web scraper using crawl4ai.
"""
import asyncio
from datetime import datetime
from typing import List, Dict
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from config import HEADLESS_MODE, SCRAPE_TIMEOUT
from utils.logger import get_logger

logger = get_logger(__name__)


async def scrape_urls(urls: List[str]) -> List[Dict]:
    """Scrape content from URLs."""
    logger.info(f"Scraping {len(urls)} URLs")
    results = []
    
    browser_config = BrowserConfig(
        headless=HEADLESS_MODE,
        extra_args=['--disable-gpu', '--no-sandbox']
    )
    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        wait_until="domcontentloaded",
        page_timeout=30000
    )
    
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            for url in urls:
                try:
                    logger.debug(f"Scraping: {url}")
                    result = await asyncio.wait_for(
                        crawler.arun(url=url, config=crawler_config),
                        timeout=float(SCRAPE_TIMEOUT)
                    )
                    
                    if result.success:
                        content = result.markdown or result.cleaned_html or ""
                        if content:
                            results.append({
                                "url": url,
                                "content": content[:10000],
                                "scraped_at": datetime.utcnow().isoformat()
                            })
                            logger.debug(f"OK: {url} ({len(content)} chars)")
                        else:
                            logger.warning(f"Empty: {url}")
                    else:
                        logger.warning(f"Failed: {url}")
                        
                except asyncio.TimeoutError:
                    logger.warning(f"Timeout: {url}")
                except Exception as e:
                    logger.error(f"Error {url}: {e}")
                    
    except Exception as e:
        logger.error(f"Browser error: {e}")
    
    logger.info(f"Scraped {len(results)}/{len(urls)} successfully")
    return results


def scrape(urls: List[str]) -> List[Dict]:
    """Sync wrapper for scraping."""
    return asyncio.run(scrape_urls(urls))
