from app.services.text_splitter.recursive_splitter import recursive_splitter
from app.services.text_splitter.character_splitter import character_splitter
from app.services.text_splitter.token_splitter import token_splitter
from app.utils.envs import Envs


_SPLITTER_MAP = {
    "recursive": recursive_splitter,
    "character": character_splitter,
    "token": token_splitter,
}


def get_text_splitter():
    provider = (getattr(Envs, "TEXT_SPLITTER", None) or "recursive").lower()
    
    if provider not in _SPLITTER_MAP:
        raise ValueError(f"Unsupported text splitter provider: {provider}")
    
    return _SPLITTER_MAP[provider]
