from app.services.vector_store.pinecone_vector_store import pinecone_vector_store
from app.utils.envs import Envs


_PROVIDER_MAP = {
    "pinecone": pinecone_vector_store,
}

def get_vector_store():
    provider = (getattr(Envs, "VECTOR_STORE") or "pinecone").lower()
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Unsupported vector store provider: {provider}")
    return _PROVIDER_MAP[provider]
