import os
from dotenv import load_dotenv


load_dotenv(override=True)

class Envs:
    BASE_SHL_URL: str = os.getenv("BASE_SHL_URL", "https://www.shl.com")
    SHL_PRODUCT_CATALOGUE_URL: str = os.getenv("SHL_PRODUCT_CATALOGUE_URL", "")
    EMBEDDER: str = os.getenv("EMBEDDER", "google")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY", "")
    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "pinecone")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "shl-assessments")
    TEXT_SPLITTER: str = os.getenv("TEXT_SPLITTER", "recursive")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "groq")
    SCRAPER_USER_AGENT: str = os.getenv("SCRAPER_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    RETRIEVER_PROVIDER: str = os.getenv("RETRIEVER_PROVIDER", "mmr")
    RERANKER_PROVIDER: str = os.getenv("RERANKER_PROVIDER", "pinecone")
    RERANKER_TOP_N: int  = int(os.getenv("RERANKER_TOP_N", "20"))
    MIN_RESULTS: int  = int(os.getenv("MIN_RESULTS", "5"))
    MAX_RESULTS: int  = int(os.getenv("MAX_RESULTS", "10"))
    TOP_K: int  = int(os.getenv("TOP_K", "50"))
    FETCH_K: int  = int(os.getenv("FETCH_K", "100"))
