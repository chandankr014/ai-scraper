"""
Configuration for the API.
"""
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).parent

# LLM Provider: "openrouter" or "groq" (defaults to groq if not set)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# Validate required keys at startup
if LLM_PROVIDER == "groq" and not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not set but LLM_PROVIDER is 'groq'")
elif LLM_PROVIDER == "openrouter" and not OPENROUTER_API_KEY:
    logging.warning("OPENROUTER_API_KEY not set but LLM_PROVIDER is 'openrouter'")

# Models
GROQ_MODELS = [
    "groq/compound-mini", 
    "moonshotai/kimi-k2-instruct-0905", 
    "qwen/qwen3-32b"
]
OPENROUTER_MODELS = [
    "mistralai/mistral-7b-instruct:free", 
    "meta-llama/llama-3.2-3b-instruct:free"
]

DEFAULT_GROQ_MODEL = os.getenv(
    "DEFAULT_GROQ_MODEL", 
    "groq/compound-mini")
DEFAULT_OPENROUTER_MODEL = os.getenv(
    "DEFAULT_OPENROUTER_MODEL", 
    "mistralai/mistral-7b-instruct:free")

# Scraping
HEADLESS_MODE = os.getenv("HEADLESS_MODE", "true").lower() == "true"
SCRAPE_TIMEOUT = int(os.getenv("SCRAPE_TIMEOUT", "30"))

# API
API_VERSION = "1.0.0"
