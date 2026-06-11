# ✈️ AI-Assisted Trip Planner

An intelligent travel planning assistant powered by a **ReAct agentic workflow**, large language models, and real-time data sources. Ask it anything about a destination and get a fully structured, exportable travel plan.

---

## 🌟 Features

- 🤖 **Agentic AI** — ReAct graph-based reasoning via LangGraph
- 🔍 **Multi-source search** — Tavily search with Google Places fallback
- 💱 **Live currency conversion** — real-time exchange rates
- 📍 **Attraction discovery** — powered by Tavily Search
- 📄 **Exportable plans** — auto-saves every response as a `.md` file
- 📜 **Plan history** — retrieve and download previously generated plans
- ⚡ **Fast API backend** — async FastAPI with CORS support

---

## 🏗️ Project Structure

```
ai-trip-planner/
├── agent/
│   └── agent_workflow.py       # LangGraph ReAct graph builder
├── configs/
│   ├── config.yaml             # Agent Configurations
├── exception/
│   ├── exceptions.py           # Custom Exception Handling
├── prompts/
│   ├── prompt.py               # System prompt for ai agent
├── tools/
│   ├── currency_conversion.py  # Currency Converter Tools
│   └── expense_calculator.py   # Expenses Calculation Tools
│   └── place_search.py         # Place Search Tools
│   └── weather_information.py  # Weather Information Tools
├── utils/
│   ├── calculate_expenses.py   # Expenses Calculation Service
│   └── config_loader.py        # Config Loader Service
│   └── currency_converter.py   # Currency Converter Service
│   └── model_loader.py         # Model Loader Service
│   └── place_info_search.py    # Place Search Service
│   └── save_to_document.py     # Document Save Service
│   └── weather_info.py         # Weather Information Service
├── requirements.txt            # Python packages for the project
├── app.py                      # FastAPI application
├── output/                     # Auto-generated travel plan .md files
├── .env                        # API keys (not committed)
├── .env.example                # Example env file
├── pyproject.toml              # uv project dependencies
└── README.md
```

---

## ⚙️ Prerequisites

- [Python 3.14+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — fast Python package manager

Install `uv` if you don't have it:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 🚀 Setup & Installation

### 1. Clone the repository

```bash
mkdir ai-trip-planner
cd ai-trip-planner
git clone https://github.com/aryanfredericks/AI_Trip_Planner.git .
```

### 2. Create and activate a virtual environment

```bash
uv init
uv venv --python 3.14
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install Packages

```bash
uv add -r requirements.txt
```

### 4. Configure your API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# LLM
GROQ_API_KEY=your_groq_api_key

# Search
TAVILY_API_KEY=your_tavily_api_key

# Places
GPLACES_API_KEY=your_google_places_api_key
GOOGLE_API_KEY=your_google_api_key
FOURSQUARE_API_KEY=your_foursquare_api_key

# Currency
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key

# Weather
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

> 🔑 See [API Keys Guide](#-api-keys-guide) below for how to obtain each key.

### 5. Configure your model

Edit `config.yaml` to set your preferred LLM provider and model:

```yaml
llm:
  groq:
    provider: "groq"
    model_name: "deepseek-r1-distill-llama-70b"
```

---

## ▶️ Running the Application

Start the FastAPI server with `uvicorn`:

```bash
uvicorn app:app --reload
```

The API will be available at **`http://localhost:8000`**

For a custom host/port:
```bash
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

> The `--reload` flag enables hot-reloading during development. Remove it for production.

---

## 📡 API Endpoints

### `POST /query`
Submit a travel planning question and receive a full AI-generated plan.

**Request:**
```json
{
  "question": "Plan a 5-day trip to Tokyo for 2 people in October"
}
```

**Response:**
```json
{
  "answer": "# 🌍 AI Travel Plan\n\n...",
  "document_path": "./output/AI_Trip_Planner_2026-06-11_10-30-00.md",
  "download_url": "/download/AI_Trip_Planner_2026-06-11_10-30-00.md"
}
```

---

### `GET /download/{filename}`
Download a previously generated travel plan as a `.md` file.

```
GET /download/AI_Trip_Planner_2026-06-11_10-30-00.md
```

---

### `GET /history`
List all previously generated travel plans.

**Response:**
```json
{
  "documents": [
    {
      "filename": "AI_Trip_Planner_2026-06-11_10-30-00.md",
      "download_url": "/download/AI_Trip_Planner_2026-06-11_10-30-00.md"
    }
  ]
}
```

---

### 📖 Interactive Docs

FastAPI ships with built-in API documentation. Once running, visit:

| UI | URL |
|---|---|
| Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---

## 🔑 API Keys Guide

| Key | Provider | Free Tier | Get it here |
|---|---|---|---|
| `GROQ_API_KEY` | Groq | ✅ Free | [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | Tavily | ✅ Free (1,000 searches/mo) | [tavily.com](https://tavily.com) |
| `GPLACES_API_KEY` | Google Places | ✅ Free tier (billing req.) | [console.cloud.google.com](https://console.cloud.google.com) |
| `GOOGLE_API_KEY` | Google AI (Gemini) | ✅ Free tier | [aistudio.google.com](https://aistudio.google.com) |
| `FOURSQUARE_API_KEY` | Foursquare | ✅ 500 calls/mo free | [location.foursquare.com/developer](https://location.foursquare.com/developer) |
| `EXCHANGE_RATE_API_KEY` | ExchangeRate-API | ✅ 1,500 requests/mo free | [exchangerate-api.com](https://www.exchangerate-api.com) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) + [LangChain](https://langchain.com/) |
| LLM Provider | [Groq](https://groq.com/) (DeepSeek R1 / Llama 70B) |
| Web Search | [Tavily](https://tavily.com/) |
| Places Data | Google Places API + Foursquare + Tavily Search |
| Currency Data | ExchangeRate-API |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Built with ❤️ by Aryan.
</div>