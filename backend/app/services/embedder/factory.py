from app.services.embedder.google_embedder import google_embedder
from app.utils.envs import Envs


_PROVIDER_MAP = {
    "google": {
        "embedder": google_embedder,
        "dimension": 3072,
    },
}

def get_embedder():
    provider = (getattr(Envs, "EMBEDDER") or "google").lower()
    
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Unsupported embedder provider: {provider}")
    
    return _PROVIDER_MAP[provider]