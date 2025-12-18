import os
from dotenv import load_dotenv


load_dotenv(override=True)

class Envs:
    BASE_SHL_URL: str = os.getenv("BASE_SHL_URL", "https://www.shl.com")
    SHL_PRODUCT_CATALOGUE_URL: str = os.getenv("SHL_PRODUCT_CATALOGUE_URL", "")
    EMBEDDER: str = os.getenv("EMBEDDER", "google")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    VECTOR_STORE: str = os.getenv("VECTOR_STORE", "pinecone")
    PINECONE_API_KEY: str = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME: str = os.getenv("PINECONE_INDEX_NAME", "shl-assessments")
    TEXT_SPLITTER: str = os.getenv("TEXT_SPLITTER", "recursive")
    SCRAPER_USER_AGENT: str = os.getenv("SCRAPER_USER_AGENT", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
