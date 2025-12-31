# 🤖 AI Scraper

An intelligent API that searches the web, scrapes content, and extracts key information using LLMs.

![Workflow](image.png)

## ✨ Features

- **Google Search Integration** — Find relevant URLs via Custom Search API
- **Smart Web Scraping** — Headless browser extraction using crawl4ai
- **LLM-Powered Analysis** — Extract insights with Groq or OpenRouter models
- **RESTful API** — Clean FastAPI endpoints with auto-documentation

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start server
python main.py
```

**Server:** `http://127.0.0.1:5001`

---

## 📡 API Endpoints

### Search & Extract
Search the web and extract information from results.

```bash
POST /api/search
```

```json
{
  "query": "latest tech news 2024",
  "max_urls": 5,
  "model": "groq/compound-mini"
}
```

### Extract from URLs
Extract information from specific URLs.

```bash
POST /api/extract
```

```json
{
  "urls": ["https://example.com/article"],
  "model": "groq/compound-mini"
}
```

### Health Check
```bash
GET /api/health
```

---

## 📋 Response Format

```json
{
  "urls_processed": 3,
  "urls": ["https://..."],
  "summary": "Key findings and insights...",
  "model_used": "groq/compound-mini",
  "processing_time": 8.5
}
```

---

## ⚙️ Configuration

Create `.env` from `.env.example`:

```env
# LLM Provider: "groq" or "openrouter"
LLM_PROVIDER=groq

# API Keys
GROQ_API_KEY=your_groq_key
OPENROUTER_API_KEY=your_openrouter_key

# Google Custom Search
GOOGLE_SEARCH_API_KEY=your_google_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id

# Settings
HEADLESS_MODE=true
SCRAPE_TIMEOUT=30
```

### Supported Models

| Provider | Models |
|----------|--------|
| Groq | `groq/compound-mini`, `moonshotai/kimi-k2-instruct-0905`, `qwen/qwen3-32b` |
| OpenRouter | `mistralai/mistral-7b-instruct:free`, `meta-llama/llama-3.2-3b-instruct:free` |

---

## 📁 Project Structure

```
├── main.py           # FastAPI application entry
├── config.py         # Environment configuration
├── api/
│   ├── routes.py     # API endpoints
│   └── schemas.py    # Request/response models
├── core/
│   ├── search.py     # Google Custom Search API
│   ├── scraper.py    # crawl4ai web scraper
│   ├── extractor.py  # LLM content extraction
│   └── llm_client.py # Groq/OpenRouter client
├── utils/            # Logging utilities
└── answers/          # Saved API responses
```

---

## 📖 Docs

- **Swagger UI:** http://127.0.0.1:5001/docs
- **ReDoc:** http://127.0.0.1:5001/redoc

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| Scraping | crawl4ai + Playwright |
| Search | Google Custom Search API |
| LLM | Groq / OpenRouter |

---
## 🤝 Contact

For collaboration, please contact **Chandan Kumar** at [chandankr014@gmail.com](mailto:chandankr014@gmail.com).
