from typing import List
from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document

from app.services.llm.factory import get_llm
from app.services.reranker.base_reranker import BaseReranker


class LLMReranker(BaseReranker):
    def __init__(self, llm: BaseChatModel):
        self.llm = llm
        self.prompt_template = """
            Query: {query}
            Document: {page_content}
            Score relevance from 0 to 1.
            Only output the numeric score.
            """

    def rerank(self, query: str, documents: List[Document]) -> list:
        ranked_documents: list[tuple[Document, float]] = []
        for doc in documents:
            prompt = self.prompt_template.format(query=query, page_content=doc.page_content)
            score = self.llm.invoke(prompt).content
            ranked_documents.append((doc, float(score)))  # type: ignore
        
        return sorted(ranked_documents, key=lambda x: x[1], reverse=True)
    
    def get_compressor(self):  # type: ignore
        return None


llm_reranker = LLMReranker(llm=get_llm())
    