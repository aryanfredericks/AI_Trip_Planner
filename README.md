# ✈️ AI-Assisted Trip Planner

An intelligent travel planning assistant powered by a **ReAct agentic workflow**, large language models, and real-time data sources. Ask it anything about a destination and get a fully structured, exportable travel plan.

---

## 🌟 Features

- 🤖 **Agentic AI** — ReAct graph-based reasoning via LangGraph
- 🔍 **Multi-source search** — Tavily search with Google Places fallback
- 💱 **Live currency conversion** — real-time exchange rates
- 📍 **Attraction discovery** — powered by Tavily Search
- 🌤️ **Weather information** — real-time weather data via OpenWeatherMap
- 📄 **Exportable plans** — auto-saves every response as a `.md` file to Supabase Storage
- 📜 **Plan history** — per-user history stored in Supabase Postgres
- ⚡ **Fast API backend** — async FastAPI with CORS support
- 🐳 **Dockerized** — containerized for consistent deployment
- ☁️ **Cloud deployed** — hosted on AWS EC2 with CI/CD via GitHub Actions

---

## 🏗️ Project Structure

```
ai-trip-planner/
├── agent/
│   └── agent_workflow.py           # LangGraph ReAct graph builder
├── configs/
│   └── config.yaml                 # Agent configurations
├── exception/
│   └── exceptions.py               # Custom exception handling
├── prompts/
│   └── prompt.py                   # System prompt for AI agent
├── tools/
│   ├── currency_conversion.py      # Currency converter tools
│   ├── expense_calculator.py       # Expense calculation tools
│   ├── place_search.py             # Place search tools
│   └── weather_information.py      # Weather information tools
├── utils/
│   ├── calculate_expenses.py       # Expense calculation service
│   ├── config_loader.py            # Config loader service
│   ├── currency_converter.py       # Currency converter service
│   ├── model_loader.py             # Model loader service
│   ├── place_info_search.py        # Place search service
│   ├── save_to_document.py         # Document save service
│   ├── supabase_client.py          # Supabase client
│   └── weather_info.py             # Weather information service
├── .github/
│   └── workflows/
│       └── deploy.yml              # GitHub Actions CI/CD pipeline
├── Dockerfile                      # Docker build instructions
├── .dockerignore                   # Files excluded from Docker image
├── app.py                          # FastAPI application
├── requirements.txt                # Python packages
├── pyproject.toml                  # uv project dependencies
├── .env.example                    # Example environment variables
└── README.md
```

---

## ⚙️ Prerequisites

- [Python 3.14+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — fast Python package manager
- [Docker](https://docs.docker.com/get-docker/) — for containerized deployment
- [Supabase account](https://supabase.com) — for database and file storage
- [AWS account](https://aws.amazon.com) — for cloud deployment (optional for local dev)

Install `uv` if you don't have it:
```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## 🚀 Local Setup & Installation

### 1. Clone the repository

```bash
mkdir ai-trip-planner
cd ai-trip-planner
git clone https://github.com/aryanfredericks/AI_Trip_Planner.git .
```

### 2. Create and activate a virtual environment

```bash
uv venv --python 3.14
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

### 3. Install packages

```bash
uv add -r requirements.txt
```

### 4. Configure your API keys

```bash
cp .env.example .env
```

Edit `.env` with your keys:

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

# Supabase
SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_role_key
```

### 5. Configure your model

Edit `configs/config.yaml`:

```yaml
llm:
  groq:
    provider: "groq"
    model_name: "llama-3.3-70b-versatile"
```

### 6. Run the application

```bash
uvicorn app:app --reload
```

API available at **`http://localhost:8000`**

---

## 🗄️ Supabase Setup

This project uses Supabase for per-user data storage. Follow these steps to set it up.

### 1. Create a Supabase project

1. Go to [supabase.com](https://supabase.com) → New project
2. Choose a name and region → wait ~2 minutes to provision

### 2. Create the database table

Go to **SQL Editor** in your Supabase dashboard and run:

```sql
create table public.travel_plans (
    id           uuid        default gen_random_uuid() primary key,
    user_id      text        not null,
    question     text        not null,
    answer       text        not null,
    filename     text        not null,
    storage_path text        not null,
    created_at   timestamptz default now()
);

create index travel_plans_user_id_idx on public.travel_plans(user_id);
create index travel_plans_created_idx on public.travel_plans(created_at desc);

alter table public.travel_plans enable row level security;

create policy "Allow all operations"
    on public.travel_plans
    for all
    using (true)
    with check (true);
```

### 3. Create a Storage bucket

1. Go to **Storage** → **New bucket**
2. Name it `travel-plans` → set to **Private** → Create
3. Go to **SQL Editor** and run:

```sql
create policy "Allow all storage operations"
    on storage.objects
    for all
    to public
    using (bucket_id = 'travel-plans')
    with check (bucket_id = 'travel-plans');
```

### 4. Get your credentials

Go to **Settings → API** and copy:
- `Project URL` → `SUPABASE_URL`
- `service_role` secret key → `SUPABASE_SERVICE_KEY`

Add both to your `.env` file.

---

## 🐳 Running with Docker

```bash
# build the image
docker build -t ai-trip-planner .

# run with your .env file
docker run -p 8000:8000 --env-file .env ai-trip-planner

# verify it's running
curl http://localhost:8000/health
```

---

## ☁️ AWS Deployment

This project is deployed on AWS EC2 with automatic deployments via GitHub Actions.

### Architecture

```
Push to main
     ↓
GitHub Actions
     ↓
Build Docker image → Push to Docker Hub → SSH into EC2 → docker pull + restart
```

### 1. Set up GitHub secrets

Go to `repo → Settings → Secrets and variables → Actions` and add:

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_TOKEN` | Docker Hub access token (Read & Write) |
| `EC2_HOST` | Your EC2 Elastic IP address |
| `EC2_SSH_KEY` | Contents of your `.pem` key file |

### 2. Create a Docker Hub access token

1. Go to [hub.docker.com](https://hub.docker.com) → Account Settings → Personal access tokens
2. Click **Generate new token** → set permissions to **Read & Write**
3. Copy the token → add as `DOCKER_TOKEN` GitHub secret

### 3. Launch an EC2 instance

1. AWS Console → EC2 → **Launch Instance**
2. AMI: **Ubuntu 24.04 LTS**
3. Instance type: `t3.small` (recommended)
4. Create a new key pair → download the `.pem` file
5. Security group inbound rules:

| Port | Source | Purpose |
|---|---|---|
| 22 | Your IP | SSH |
| 8000 | 0.0.0.0/0 | FastAPI |

### 4. Assign an Elastic IP (permanent IP)

1. EC2 → **Elastic IPs** → Allocate Elastic IP
2. Select it → **Actions → Associate** → select your instance
3. Update `EC2_HOST` GitHub secret with this IP

### 5. First-time EC2 setup

```bash
# SSH into your instance
ssh -i ~/.ssh/your-key.pem ubuntu@your-elastic-ip

# install Docker
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable docker && sudo systemctl start docker
sudo usermod -aG docker ubuntu
newgrp docker

# create your .env file on the server (never committed to git)
nano /home/ubuntu/.env
# paste all your API keys and save with Ctrl+X → Y → Enter
```

### 6. Deploy

Push to `main` — GitHub Actions handles everything automatically:

```bash
git add .
git commit -m "deploy"
git push origin main
```

Watch the deployment at `repo → Actions` tab. Completes in ~3 minutes.

### 7. Verify deployment

```bash
docker ps                          # container should be running
docker logs travel-planner         # check for errors
curl http://localhost:8000/health  # should return {"status":"ok"}
```

### Rollback to a previous version

```bash
docker stop travel-planner && docker rm travel-planner
docker run -d \
  --name travel-planner \
  --restart always \
  -p 8000:8000 \
  --env-file /home/ubuntu/.env \
  yourdockerhub/ai-trip-planner:<commit-sha>
```

---

## 📡 API Endpoints

All endpoints require an `x-user-id` header (device ID sent automatically by the Flutter app).

### `POST /query`

```json
// Request
{ "question": "Plan a 5-day trip to Tokyo for 2 people in October" }

// Response
{
  "answer": "# 🌍 AI Travel Plan\n\n...",
  "filename": "AI_Trip_Planner_2026-06-11_10-30-00.md",
  "download_url": "/download/AI_Trip_Planner_2026-06-11_10-30-00.md"
}
```

### `GET /history`

Returns all travel plans for the requesting user from Supabase.

```json
{
  "documents": [
    {
      "filename": "AI_Trip_Planner_2026-06-11_10-30-00.md",
      "question": "Plan a 5-day trip to Tokyo...",
      "created_at": "2026-06-11T10:30:00",
      "download_url": "/download/AI_Trip_Planner_2026-06-11_10-30-00.md"
    }
  ]
}
```

### `GET /download/{filename}`

Streams the `.md` file from Supabase Storage.

### `GET /health`

```json
{ "status": "ok" }
```

### 📖 Interactive docs

| UI | URL |
|---|---|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

---

## 🔑 API Keys Guide

| Key | Provider | Free Tier | Get it here |
|---|---|---|---|
| `GROQ_API_KEY` | Groq | ✅ Free | [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | Tavily | ✅ 1,000 searches/mo | [tavily.com](https://tavily.com) |
| `GPLACES_API_KEY` | Google Places | ✅ Free tier (billing req.) | [console.cloud.google.com](https://console.cloud.google.com) |
| `GOOGLE_API_KEY` | Google AI | ✅ Free tier | [aistudio.google.com](https://aistudio.google.com) |
| `FOURSQUARE_API_KEY` | Foursquare | ✅ 500 calls/mo | [location.foursquare.com/developer](https://location.foursquare.com/developer) |
| `EXCHANGE_RATE_API_KEY` | ExchangeRate-API | ✅ 1,500 requests/mo | [exchangerate-api.com](https://www.exchangerate-api.com) |
| `OPENWEATHERMAP_API_KEY` | OpenWeatherMap | ✅ 1,000 calls/day | [openweathermap.org/api](https://openweathermap.org/api) |
| `SUPABASE_URL` | Supabase | ✅ Free tier | [supabase.com](https://supabase.com) |
| `SUPABASE_SERVICE_KEY` | Supabase | ✅ Free tier | [supabase.com](https://supabase.com) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Orchestration | [LangGraph](https://langchain-ai.github.io/langgraph/) + [LangChain](https://langchain.com/) |
| LLM Provider | [Groq](https://groq.com/) (Llama 3.3 70B) |
| Web Search | [Tavily](https://tavily.com/) |
| Places Data | Google Places API + Foursquare + Tavily |
| Currency Data | ExchangeRate-API |
| Weather Data | OpenWeatherMap |
| Database | [Supabase](https://supabase.com/) (Postgres) |
| File Storage | Supabase Storage |
| Backend | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| Containerization | [Docker](https://www.docker.com/) |
| Cloud | [AWS EC2](https://aws.amazon.com/ec2/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) |
| Package Manager | [uv](https://docs.astral.sh/uv/) |

---

## 🤝 Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Set up your local environment following the [Local Setup](#-local-setup--installation) steps above
4. Set up your own Supabase project following the [Supabase Setup](#️-supabase-setup) steps above
5. Make your changes
6. Commit: `git commit -m 'Add my feature'`
7. Push: `git push origin feature/my-feature`
8. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Built with ❤️ by Aryan
</div>