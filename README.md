# 🌊 Flood Intelligence API

AI-powered API to extract flood-related intelligence from web sources using LLMs and web scraping.

![Workflow](image.png)

## ✨ Features

- **AI-Powered Extraction** — Uses OpenRouter/Groq LLMs for intelligent analysis
- **Web Scraping** — Headless browser scraping via crawl4ai
- **Smart Search** — Auto-rephrases queries for better results
- **Structured Output** — Returns organized flood intelligence data
- **Multi-Model Support** — Switch between free LLM models

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Configure API key
# Edit .env and add: OPENROUTER_API_KEY=your_key

# Run server
python main.py
```

Server starts at: `http://127.0.0.1:5001`

---

## 📡 API Usage

### Search for Flood Intelligence

```bash
curl -X POST http://127.0.0.1:5001/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "flood news chennai 2024", "max_urls": 5}'
```

### Extract from Specific URLs

```bash
curl -X POST http://127.0.0.1:5001/api/extract \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/news"]}'
```

### Health Check

```bash
curl http://127.0.0.1:5001/api/health
```

---

## 📋 Response Structure

```json
{
  "urls_processed": 3,
  "summary": "Extracted intelligence...",
  "intelligence": {
    "flood_status": { "severity": "moderate", "trend": "stable" },
    "affected_areas": [...],
    "key_findings": [...],
    "recommendations": [...]
  },
  "model_used": "meta-llama/llama-3.2-3b-instruct:free",
  "processing_time": 12.5
}
```

---

## ⚙️ Configuration

Create a `.env` file:

```env
# Required
OPENROUTER_API_KEY=your_key_here

# Optional
LLM_PROVIDER=groq          # or "openrouter"
HEADLESS_MODE=true
SCRAPE_TIMEOUT=30
MAX_URLS_PER_QUERY=5
```

---

## 📁 Project Structure

```
flood_intel_api/
├── main.py           # Entry point
├── config.py         # Settings
├── api/              # FastAPI routes
├── core/             # Search, scrape, extract logic
├── answers/          # Saved responses (JSON)
└── logs/             # Application logs
```

---

## 📖 Documentation

- **Interactive Docs**: http://127.0.0.1:5001/docs
- **Detailed Guide**: See [DOC.md](DOC.md)

---

## 🛠️ Tech Stack

- **FastAPI** — Web framework
- **crawl4ai** — Web scraping
- **OpenRouter / Groq** — LLM providers
- **Playwright** — Browser automation

---

## 📝 License

MIT
