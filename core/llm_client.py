"""
LLM Client - supports Groq and OpenRouter.
"""
from openai import OpenAI
from groq import Groq
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import LLM_PROVIDER, GROQ_API_KEY, OPENROUTER_API_KEY, DEFAULT_GROQ_MODEL, DEFAULT_OPENROUTER_MODEL
from utils.logger import get_logger

logger = get_logger(__name__)

# Initialize client based on provider
_client = None
_default_model = None

try:
    if LLM_PROVIDER == "groq":
        if not GROQ_API_KEY:
            logger.error("GROQ_API_KEY is required when LLM_PROVIDER is 'groq'")
        else:
            _client = Groq(api_key=GROQ_API_KEY)
            _default_model = DEFAULT_GROQ_MODEL
            logger.info("Using Groq")
    else:
        if not OPENROUTER_API_KEY:
            logger.error("OPENROUTER_API_KEY is required when LLM_PROVIDER is 'openrouter'")
        else:
            _client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)
            _default_model = DEFAULT_OPENROUTER_MODEL
            logger.info("Using OpenRouter")
except Exception as e:
    logger.error(f"Failed to initialize LLM client: {e}")


def chat(prompt: str, system_prompt: str = None, model: str = None) -> str:
    """Send chat request to LLM."""
    if _client is None:
        raise RuntimeError("LLM client not initialized. Check API key configuration.")
    
    model = model or _default_model
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    logger.debug(f"LLM request: {len(prompt)} chars, model={model}")
    
    response = _client.chat.completions.create(model=model, messages=messages, temperature=0.3)
    result = response.choices[0].message.content
    
    logger.debug(f"LLM response: {len(result)} chars")
    return result
