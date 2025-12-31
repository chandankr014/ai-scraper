"""
Flood Intelligence API - Extract information from web pages.
"""
import os
import uvicorn
from fastapi import FastAPI
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from api.routes import router
from config import API_VERSION
from utils.logger import get_logger, setup_logging

# Initialize logging at startup
setup_logging()
logger = get_logger(__name__)

# Server configuration
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "5001"))

app = FastAPI(
    title="Web Intelligence API",
    description="Extract key information from web pages using AI",
    version=API_VERSION
)

app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    return {
        "name": "Web Intelligence API",
        "version": API_VERSION,
        "endpoints": {
            "health": "/api/health",
            "extract": "/api/extract (POST)"
        }
    }


if __name__ == "__main__":
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
