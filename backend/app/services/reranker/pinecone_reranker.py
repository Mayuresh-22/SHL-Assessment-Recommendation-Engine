from typing import List, Tuple
from langchain_core.documents import Document
from langchain_pinecone import PineconeRerank

from app.services.reranker.base_reranker import BaseReranker
from app.utils.envs import Envs


class PineconeReranker(BaseReranker):
    def __init__(self, model: str = "pinecone-rerank-v0"):
        self.reranker = PineconeRerank(model=model, top_n=Envs.RERANKER_TOP_N)

    def rerank(self, query: str, documents: List[Document]) -> List[Tuple[Document, float]]:
        reranked_docs = self.reranker.compress_documents(documents, query)
        ranked_documents: List[Tuple[Document, float]] = []
        
        for doc in reranked_docs:
            score = doc.metadata.get("relevance_score", 0.0)
            ranked_documents.append((doc, float(score)))
        
        return sorted(ranked_documents, key=lambda x: x[1], reverse=True)


pinecone_reranker = PineconeReranker()
