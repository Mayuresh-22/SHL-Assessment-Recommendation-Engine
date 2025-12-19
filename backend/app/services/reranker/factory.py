from app.services.reranker.llm_reranker import llm_reranker
from app.services.reranker.pinecone_reranker import pinecone_reranker
from app.services.reranker.cohere_reranker import cohere_reranker
from app.utils.envs import Envs


_PROVIDER_MAP = {
    "llm": llm_reranker,
    "pinecone": pinecone_reranker,
    "cohere": cohere_reranker,
}

def get_reranker():
    provider = (getattr(Envs, "RERANKER_PROVIDER", None) or "pinecone").lower()
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Unsupported reranker provider: {provider}")
    return _PROVIDER_MAP[provider]
