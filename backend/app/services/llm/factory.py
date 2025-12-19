from app.services.llm.google_llm import google_llm
from app.utils.envs import Envs


_PROVIDER_MAP = {
    "google": google_llm,
}

def get_llm():
    provider = (getattr(Envs, "LLM_PROVIDER", None) or "google").lower()
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    return _PROVIDER_MAP[provider]
