from langchain_core.documents import Document, BaseDocumentCompressor

from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseReranker(ABC):
    @abstractmethod
    def rerank(self, query: str, documents: list) -> List[Tuple[Document, float]]:
        pass
    
    @abstractmethod
    def get_compressor(self) -> BaseDocumentCompressor:
        pass
