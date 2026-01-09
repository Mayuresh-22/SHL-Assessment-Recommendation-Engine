# SHL Assessment Recommendation Engine

An AI-powered recommendation system that suggests the most relevant SHL assessments based on natural language queries, job descriptions, or hiring requirements. Built with a FastAPI backend and React frontend, leveraging semantic search, LLM-powered query transformation, and intelligent reranking.

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.125+-009688?logo=fastapi)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector%20DB-purple)
![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-3.4-38B2AC?logo=tailwindcss)

---

## Live (See it in action)
Web app: https://mayuresh-shl-assessment-recommendation-frontend.pages.dev

---

## Some screenshots

<img width="1470" height="1034" alt="SHL Assessment Recommendation System" src="https://github.com/user-attachments/assets/0a3d486a-23ea-4767-b0a0-920ff6ba8d59" />
<img width="1458" height="1034" alt="SHL Assessment Recommendation System" src="https://github.com/user-attachments/assets/d84b6c70-5b4e-468f-8787-1bc92b1af5c4" />


## Overview

This system helps HR professionals and hiring managers find the most suitable SHL assessments by:

- **Understanding natural language** - Describe your hiring needs in plain English
- **Semantic matching** - Finds assessments based on meaning, not just keywords
- **Intelligent ranking** - Multi-stage pipeline ensures the best recommendations surface first
- **Balanced results** - Delivers diverse assessment types while respecting user preferences

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (React + Vite)                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │  Query Input  →  API Call  →  Results Table (Assessment Recommendations) ││
│  └─────────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            BACKEND (FastAPI)                                 │
│  ┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌─────────┐ │
│  │    Query      │ →  │   Retriever   │ →  │   Reranker    │ →  │Balancer │ │
│  │  Transformer  │    │  (MMR/Pinecone)│    │(Pinecone/Cohere)│  │         │ │
│  │   (LLM)       │    │               │    │               │    │         │ │
│  └───────────────┘    └───────────────┘    └───────────────┘    └─────────┘ │
│         │                     │                                              │
│         ▼                     ▼                                              │
│  ┌───────────────┐    ┌───────────────┐                                      │
│  │  Google/Groq  │    │   Pinecone    │                                      │
│  │     LLM       │    │  Vector Store │                                      │
│  └───────────────┘    └───────────────┘                                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Recommendation Pipeline

```
User Query → Query Transformer → Retriever → Reranker → Balancer → Recommendations
```

1. **Query Transformation**: LLM rewrites input into an optimized search query and infers preferences (test types, duration)
2. **Retrieval**: MMR retriever fetches semantically similar assessments with diversity optimization
3. **Reranking**: Results are reranked using Pinecone/Cohere for relevance scoring
4. **Balancing**: Greedy selection ensures diverse recommendations across test types

---

## Features

### Backend
- **Semantic Search** - Vector-based similarity search using Google embeddings
- **LLM Query Transformation** - Converts natural language to optimized search queries
- **Multi-Stage Pipeline** - Retrieval → Reranking → Balancing for high-quality results
- **Pluggable Components** - Factory pattern for LLMs, embedders, rerankers, retrievers
- **Evaluation Framework** - Built-in tools for measuring Recall@K metrics
- **Data Ingestion** - Automated scraping and indexing of SHL assessment catalog

### Frontend
- **Modern UI** - Clean, responsive interface with Tailwind CSS
- **Real-time Search** - Instant recommendations as you type
- **Rich Results Table** - Displays assessment name, type, duration, remote/adaptive support
- **Loading States** - Smooth user experience with loading indicators
- **Error Handling** - Graceful error messages and recovery

---

## Project Structure

```
SHL-Assessment-Recommendation-Engine/
├── README.md                      # This file
├── backend/
│   ├── main.py                    # Application entrypoint
│   ├── config.json                # Data ingestion configuration
│   ├── pyproject.toml             # Python dependencies
│   └── app/
│       ├── constants/             # LLM prompts and system messages
│       ├── evaluation/            # Evaluation tools (Recall@K)
│       ├── pydantic_models/       # Data models
│       ├── services/
│       │   ├── api/               # FastAPI routes
│       │   ├── balancer/          # Result balancing
│       │   ├── embedder/          # Embedding providers
│       │   ├── ingester/          # Data ingestion pipeline
│       │   ├── llm/               # LLM providers (Google, Groq)
│       │   ├── query/             # Query transformation
│       │   ├── recommender/       # Recommendation orchestrator
│       │   ├── reranker/          # Reranking providers
│       │   ├── retriever/         # Retrieval strategies
│       │   ├── scraper/           # SHL catalog scrapers
│       │   ├── text_splitter/     # Document chunking
│       │   └── vector_store/      # Vector database
│       └── utils/                 # Configuration utilities
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx                # Main application component
        ├── main.jsx               # React entry point
        └── index.css              # Global styles
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, Vite, Tailwind CSS |
| **Backend** | FastAPI, Python 3.11+ |
| **Vector Store** | Pinecone |
| **LLM Providers** | Google Gemini, Groq |
| **Embeddings** | Google Generative AI |
| **Rerankers** | Pinecone, Cohere, LLM-based |
| **Data Processing** | LangChain, Pandas |

---

## Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- API keys for: Google AI, Groq, Pinecone, Cohere

### Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Create .env file
cp .env.example .env  # Edit with your API keys
```

**Backend Environment Variables (.env)**:

```env
# Required API Keys
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
COHERE_API_KEY=your_cohere_api_key

# Configuration
PINECONE_INDEX_NAME=shl-assessments
LLM_PROVIDER=groq                  # Options: groq, google
EMBEDDER=google
VECTOR_STORE=pinecone
RETRIEVER_PROVIDER=mmr             # Options: mmr, vanila
RERANKER_PROVIDER=pinecone         # Options: pinecone, cohere, llm

# Retrieval Parameters
TOP_K=50
FETCH_K=100
LAMBDA_MULT=0.7
RERANKER_TOP_N=20
MIN_RESULTS=5
MAX_RESULTS=10
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env_example .env  # Edit with backend URL
```

**Frontend Environment Variables (.env)**:

```env
VITE_API_URL=http://localhost:8000
```

---

## Running the Application

### Start Backend Server

```bash
cd backend
uv run main.py
```

The API will be available at `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health/` | GET | Health check |
| `/recommend/` | POST | Get assessment recommendations |

### Example Request

```bash
curl -X POST "http://localhost:8000/recommend/" \
  -H "Content-Type: application/json" \
  -d '{"query": "Need a quick test for junior Python developers"}'
```

### Example Response

```json
{
  "recommended_assessments": [
    {
      "url": "https://www.shl.com/solutions/products/...",
      "name": "Python Programming Test",
      "description": "Measures Python programming skills...",
      "duration": 25,
      "remote_support": "Yes",
      "adaptive_support": "No",
      "test_type": ["Knowledge & Skills"]
    }
  ]
}
```

---

## Experiments & Evaluation

### Approach

The system was iteratively refined based on evaluation metrics. Key experiments included:

**Document Representation:**
- Initial approach used chunked/split documents for ingestion
- Observed severe degradation—unrelated assessments with similar metadata (job levels, categories) were incorrectly associated
- Final approach: Each assessment treated as a single semantic unit without chunking, resulting in significant retrieval improvement

**Query Transformation:**
- Evolved from simple rewriting to structured instructions with SHL-style query templates
- Added few-shot examples from different test categories to reduce bias
- Query intentionally phrased to match assessment catalog descriptions for better semantic alignment

**Rerankers Tested:**
- Pinecone BGE Reranker
- Pinecone Reranker  
- Cohere Rerank (final choice—showed slight improvements)

**Parameter Tuning:**

| Parameter | Values Tested | Finding |
|-----------|---------------|---------|
| TOP_K | 50, 100 | Higher values increased latency without accuracy gains |
| FETCH_K | 100, 250 | MMR's iterative nature caused latency spikes at 250 |
| LAMBDA_MULT | 0.7, 1.0 | 0.7 balanced relevance and diversity |

### Evaluation Results

Evaluated on SHL-provided training set using Recall@K:

| Stage | Metric | Value |
|-------|--------|-------|
| Retrieval | Recall@50 | 0.50 |
| Full Pipeline | Recall@K | 0.34 |

Check query wise recall evaluation in [backend/eval_results.txt](backend/eval_results.txt)

**Observations:**
- Technical roles show higher retrieval recall than generic administrative roles
- Behavioral assessments harder to retrieve due to implicit signals in job descriptions
- Balancer intentionally trades some recall for recommendation diversity

### Run Evaluation

```bash
cd backend
uv run main.py eval
```

Results are saved to `eval_results.txt`.

### Generate Test Set Predictions

```bash
uv run main.py testset
```

Output is saved to `test_set_predictions.csv`.

---

## Assessment Test Types

| Code | Category |
|------|----------|
| A | Ability & Aptitude |
| B | Biodata & Situational Judgement |
| C | Competencies |
| D | Development & 360 |
| E | Assessment Exercises |
| K | Knowledge & Skills |
| P | Personality & Behavior |
| S | Simulations |

---

## Configuration

### Extensible Services

All services use the factory pattern for easy extension:

| Service | Env Variable | Available Providers |
|---------|--------------|---------------------|
| LLM | `LLM_PROVIDER` | `groq`, `google` |
| Embedder | `EMBEDDER` | `google` |
| Reranker | `RERANKER_PROVIDER` | `pinecone`, `cohere`, `llm` |
| Retriever | `RETRIEVER_PROVIDER` | `mmr`, `vanila` |
| Vector Store | `VECTOR_STORE` | `pinecone` |

See [backend/README.md](backend/README.md) for detailed extension guides.

---

## License

This project is developed by [Mayuresh Choudhary](https://www.linkedin.com/in/mayureshchoudhary/) as a submission for the GenAI Task: Build an SHL Assessment Recommendation System.

---

## Author

Developed by **[Mayuresh Choudhary](https://www.linkedin.com/in/mayureshchoudhary/)**
