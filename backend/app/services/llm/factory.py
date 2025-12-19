from langchain_core.language_models import BaseChatModel

from app.services.llm.google_llm import google_llm
from app.services.llm.groq_llm import groq_llm
from app.utils.envs import Envs


_PROVIDER_MAP = {
    "google": google_llm,
    "groq": groq_llm,
}

def get_llm() -> BaseChatModel:
    provider = (getattr(Envs, "LLM_PROVIDER", None) or "groq").lower()
    if provider not in _PROVIDER_MAP:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    return _PROVIDER_MAP[provider]
