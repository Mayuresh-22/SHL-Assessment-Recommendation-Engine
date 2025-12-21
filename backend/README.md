# SHL Assessment Recommendation Engine - Backend

A sophisticated AI-powered recommendation system that suggests the most relevant SHL assessments based on natural language queries, job descriptions, or hiring requirements. The system uses semantic search, LLM-powered query transformation, and intelligent reranking to deliver accurate and balanced assessment recommendations.

## Features

- **Semantic Search**: Vector-based similarity search using embeddings for accurate assessment retrieval
- **LLM Query Transformation**: Converts natural language inputs into optimized search queries
- **Multi-Stage Pipeline**: Retrieval → Reranking → Balancing for high-quality recommendations
- **Configurable Components**: Pluggable LLMs, embedders, rerankers, and retrievers via factory pattern
- **Evaluation Framework**: Built-in tools for measuring retrieval and pipeline performance
- **Data Ingestion Pipeline**: Automated scraping and indexing of SHL assessment catalog

## Tech Stack

- **Framework**: FastAPI
- **Vector Store**: Pinecone
- **LLM Providers**: Google Gemini, Groq
- **Embeddings**: Google Generative AI
- **Rerankers**: Pinecone, Cohere, LLM-based
- **Language**: Python 3.11+

## Project Structure

```
backend/
├── main.py                    # Application entrypoint
├── config.json                # Data ingestion configuration
├── pyproject.toml             # Project dependencies
├── app/
│   ├── constants/
│   │   └── strings.py         # LLM prompts and system messages
│   ├── evaluation/
│   │   ├── evaluator.py       # Main evaluation orchestrator
│   │   ├── eval_retriever.py  # Retriever evaluation (Recall@K)
│   │   ├── eval_reranker.py   # Full pipeline evaluation
│   │   └── test_set_recommendation.py  # Test set prediction generator
│   ├── pydantic_models/
│   │   └── data_model.py      # Data models (IndividualTest, TransformedQuery, etc.)
│   ├── services/
│   │   ├── api/
│   │   │   ├── main.py        # FastAPI app initialization
│   │   │   └── routes/
│   │   │       ├── health.py  # Health check endpoint
│   │   │       └── recommend.py  # Recommendation endpoint
│   │   ├── balancer/
│   │   │   └── balancer.py    # Result balancing with diversity penalties
│   │   ├── embedder/
│   │   │   ├── factory.py     # Embedder factory
│   │   │   └── google_embedder.py
│   │   ├── ingester/
│   │   │   └── data_ingester.py  # Data ingestion pipeline
│   │   ├── llm/
│   │   │   ├── factory.py     # LLM factory
│   │   │   ├── google_llm.py  # Google Gemini integration
│   │   │   └── groq_llm.py    # Groq integration
│   │   ├── query/
│   │   │   └── query_transformer.py  # Query rewriting and intent inference
│   │   ├── recommender/
│   │   │   └── recommender.py # Main recommendation orchestrator
│   │   ├── reranker/
│   │   │   ├── base_reranker.py  # Abstract reranker interface
│   │   │   ├── factory.py     # Reranker factory
│   │   │   ├── cohere_reranker.py
│   │   │   ├── llm_reranker.py
│   │   │   └── pinecone_reranker.py
│   │   ├── retriever/
│   │   │   ├── factory.py     # Retriever factory
│   │   │   ├── mmr_retriever.py   # MMR (Maximal Marginal Relevance)
│   │   │   └── vanila_retriever.py
│   │   ├── scraper/
│   │   │   ├── base_scraper.py
│   │   │   ├── catalogue_scraper.py  # SHL catalog page scraper
│   │   │   └── assessment_scraper.py # Individual assessment scraper
│   │   ├── text_splitter/
│   │   │   ├── factory.py
│   │   │   ├── character_splitter.py
│   │   │   ├── recursive_splitter.py
│   │   │   └── token_splitter.py
│   │   └── vector_store/
│   │       ├── factory.py
│   │       └── pinecone_vector_store.py
│   └── utils/
│       ├── config.py          # Config file loader
│       └── envs.py            # Environment variables
```

## Installation

1. **Clone the repository** and navigate to the backend folder:
   ```bash
   cd backend
   ```

2. **Install dependencies** using uv (recommended) or pip:
   ```bash
   uv sync
   # or
   pip install -e .
   ```

3. **Set up environment variables** by creating a `.env` file:
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
   TOP_K=50                           # Number of documents to retrieve
   FETCH_K=100                        # Documents fetched before MMR
   LAMBDA_MULT=0.7                    # MMR diversity parameter
   RERANKER_TOP_N=20                  # Documents passed to reranker
   MIN_RESULTS=5                      # Minimum recommendations returned
   MAX_RESULTS=10                     # Maximum recommendations returned
   
   # Scraping
   SHL_PRODUCT_CATALOGUE_URL=https://www.shl.com/products/product-catalog/?start={page}&type=1
   BASE_SHL_URL=https://www.shl.com/solutions
   ```

## Usage

### Running the API Server

```bash
python main.py
# or
uv run main.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health/` | GET | Health check |
| `/recommend/` | POST | Get assessment recommendations |

#### Recommendation Request

```bash
curl -X POST "http://localhost:8000/recommend/" \
  -H "Content-Type: application/json" \
  -d '{"query": "Need a quick test for junior Python developers"}'
```

#### Response Format

```json
[
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
```

### Running Evaluation

Evaluate the retriever and full pipeline performance:

```bash
python main.py eval
# or
uv run main.py eval
```

Results are saved to `eval_results.txt` with Recall@K metrics for:
- **Retriever**: Measures raw retrieval quality
- **Full Pipeline**: Retriever + Reranker + Balancer performance

### Generating Test Set Predictions

Generate recommendations for an unlabeled test set:

```bash
python main.py testset
# or
uv run main.py testset
```

Output is saved to `test_set_predictions.csv`.

### Data Ingestion

To scrape and ingest SHL assessment data into the vector store:

1. Enable ingestion in `config.json`:
   ```json
   {
     "DATA_INGESTION": true,
     "DATA_INGESTION_START_FROM_BATCH": 0,
     "DATA_INGESTION_END_AT": 377,
     "DATA_INGESTION_BATCH_SIZE": 12,
     "DATA_INGESTION_TOTAL_BATCHES": 32,
     "DATA_INGESTION_START_FRESH": false,
     "DATA_INGESTION_WITH_SPLIT": false
   }
   ```

2. Run the application:
   ```bash
   python main.py
   ```

The ingestion process supports resuming from a specific batch if interrupted.

## How It Works

### Recommendation Pipeline

```
User Query → Query Transformer → Retriever → Reranker → Balancer → Recommendations
```

1. **Query Transformation**: LLM rewrites the input into a test-catalog-style query and infers:
   - Preferred test types (Ability, Personality, Knowledge, etc.)
   - Duration preference (short/medium/long)

2. **Retrieval**: MMR retriever fetches semantically similar assessments from Pinecone with diversity optimization

3. **Reranking**: Results are reranked using Pinecone/Cohere reranker for relevance scoring

4. **Balancing**: Greedy selection with penalties ensures diverse recommendations across test types while respecting user preferences

### Assessment Test Types

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

## Configuration

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER` | `groq` | LLM provider (groq, google) |
| `RETRIEVER_PROVIDER` | `mmr` | Retriever type (mmr, vanila) |
| `RERANKER_PROVIDER` | `pinecone` | Reranker provider (pinecone, cohere, llm) |
| `TOP_K` | `50` | Documents to retrieve |
| `FETCH_K` | `100` | MMR fetch pool size |
| `LAMBDA_MULT` | `0.7` | MMR diversity (0=max diversity, 1=max relevance) |
| `RERANKER_TOP_N` | `20` | Documents for reranking |
| `MIN_RESULTS` | `5` | Minimum recommendations |
| `MAX_RESULTS` | `10` | Maximum recommendations |

## Development

### Extensible Services

The following services use the factory pattern and can be extended with new providers:

| Service | Location | Factory | Env Variable | Current Providers |
|---------|----------|---------|--------------|-------------------|
| **LLM** | `app/services/llm/` | `factory.py` | `LLM_PROVIDER` | `groq`, `google` |
| **Embedder** | `app/services/embedder/` | `factory.py` | `EMBEDDER` | `google` |
| **Reranker** | `app/services/reranker/` | `factory.py` | `RERANKER_PROVIDER` | `pinecone`, `cohere`, `llm` |
| **Retriever** | `app/services/retriever/` | `factory.py` | `RETRIEVER_PROVIDER` | `mmr`, `vanila` |
| **Vector Store** | `app/services/vector_store/` | `factory.py` | `VECTOR_STORE` | `pinecone` |
| **Text Splitter** | `app/services/text_splitter/` | `factory.py` | `TEXT_SPLITTER` | `recursive`, `character`, `token` |

### Adding a New Provider

#### 1. LLM Provider

```python
# app/services/llm/openai_llm.py
from langchain_openai import ChatOpenAI
from app.pydantic_models.data_model import LLMStructuredOutput

openai_llm = ChatOpenAI(model="gpt-4").with_structured_output(LLMStructuredOutput)
```

```python
# app/services/llm/factory.py - Add to _PROVIDER_MAP
_PROVIDER_MAP = {
    "google": google_llm,
    "groq": groq_llm,
    "openai": openai_llm,  # Add new provider
}
```

#### 2. Embedder Provider

```python
# app/services/embedder/openai_embedder.py
from langchain_openai import OpenAIEmbeddings

openai_embedder = OpenAIEmbeddings(model="text-embedding-3-large")
```

```python
# app/services/embedder/factory.py - Add to _PROVIDER_MAP
_PROVIDER_MAP = {
    "google": {"embedder": google_embedder, "dimension": 3072},
    "openai": {"embedder": openai_embedder, "dimension": 3072},  # Add new provider
}
```

#### 3. Reranker Provider

```python
# app/services/reranker/custom_reranker.py
from app.services.reranker.base_reranker import BaseReranker

class CustomReranker(BaseReranker):
    def rerank(self, query: str, documents: list) -> List[Tuple[Document, float]]:
        # Implementation
        pass
    
    def get_compressor(self) -> BaseDocumentCompressor:
        # Implementation
        pass

custom_reranker = CustomReranker()
```

```python
# app/services/reranker/factory.py - Add to _PROVIDER_MAP
_PROVIDER_MAP = {
    "llm": llm_reranker,
    "pinecone": pinecone_reranker,
    "cohere": cohere_reranker,
    "custom": custom_reranker,  # Add new provider
}
```

#### 4. Retriever Provider

```python
# app/services/retriever/custom_retriever.py
from app.services.vector_store.factory import get_vector_store

vector_store = get_vector_store()
custom_retriever = vector_store.as_retriever(search_type="custom", search_kwargs={...})
```

```python
# app/services/retriever/factory.py - Add to _RETRIEVER_MAP
_RETRIEVER_MAP = {
    "vanila": vanila_retriever,
    "mmr": mmr_retriever,
    "custom": custom_retriever,  # Add new provider
}
```

#### 5. Vector Store Provider

```python
# app/services/vector_store/chroma_vector_store.py
from langchain_chroma import Chroma
from app.services.embedder.factory import get_embedder

chroma_vector_store = Chroma(embedding_function=get_embedder()["embedder"])
```

```python
# app/services/vector_store/factory.py - Add to _PROVIDER_MAP
_PROVIDER_MAP = {
    "pinecone": pinecone_vector_store,
    "chroma": chroma_vector_store,  # Add new provider
}
```

#### 6. Text Splitter Provider

```python
# app/services/text_splitter/semantic_splitter.py
from langchain_experimental.text_splitter import SemanticChunker

semantic_splitter = SemanticChunker(embeddings=get_embedder()["embedder"])
```

```python
# app/services/text_splitter/factory.py - Add to _SPLITTER_MAP
_SPLITTER_MAP = {
    "recursive": recursive_splitter,
    "character": character_splitter,
    "token": token_splitter,
    "semantic": semantic_splitter,  # Add new provider
}
```
