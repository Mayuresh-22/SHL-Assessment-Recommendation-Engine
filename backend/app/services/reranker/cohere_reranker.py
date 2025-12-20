import os
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_cohere import CohereRerank

from app.services.reranker.base_reranker import BaseReranker
from langchain_core.documents import BaseDocumentCompressor
from app.utils.envs import Envs


os.environ["COHERE_API_KEY"] = Envs.COHERE_API_KEY


class CohereReranker(BaseReranker):
    def __init__(self, model: str = "rerank-v4.0-pro"):
        self.reranker = CohereRerank(model=model, top_n=Envs.RERANKER_TOP_N)

    def rerank(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        reranked_docs = self.reranker.compress_documents(documents, query)
        ranked_documents: List[Tuple[Document, float]] = []
        
        for doc in reranked_docs:
            score = doc.metadata.get("relevance_score", 0.0)
            ranked_documents.append((doc, float(score)))
        
        return sorted(ranked_documents, key=lambda x: x[1], reverse=True)
    
    def get_compressor(self) -> BaseDocumentCompressor:
        return self.reranker


cohere_reranker = CohereReranker()
