from langchain_core.retrievers import BaseRetriever

from app.services.retriever.mmr_retriever import mmr_retriever
from app.services.retriever.vanila_retriever import vanila_retriever
from app.utils.envs import Envs


_RETRIEVER_MAP = {
    "vanila": vanila_retriever,
    "mmr": mmr_retriever
}

def get_retriever() -> BaseRetriever:
    provider = (getattr(Envs, "RETRIEVER_PROVIDER", "mmr")).lower()
    
    if not provider or provider not in _RETRIEVER_MAP:
        raise ValueError(f"Unsupported RETRIEVER_PROVIDER: {provider}")
     
    return _RETRIEVER_MAP[provider]
