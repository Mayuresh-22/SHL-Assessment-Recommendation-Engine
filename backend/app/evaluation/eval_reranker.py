from typing import Callable, List, Optional
from app.pydantic_models.data_model import DatasetRow, TransformedQuery
from app.services.reranker.base_reranker import BaseReranker
from app.services.balancer.balancer import ResultBalancer
from langchain_core.retrievers import BaseRetriever


class EvalReranker:
    """
    Evaluates the full pipeline: Retriever -> Reranker -> Balancer
    """
    
    def __init__(
        self, 
        retriever: BaseRetriever,
        reranker: BaseReranker,
        balancer: ResultBalancer,
        dataset: List[DatasetRow],
        transformed_queries: List[TransformedQuery],
        log_func: Optional[Callable[[str], None]] = None
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.balancer = balancer
        self.dataset = dataset
        self.transformed_queries = transformed_queries
        self._log = log_func if log_func else print
    
    def evaluate(self):
        recalls = []
        for idx, (row, transformed_query) in enumerate(zip(self.dataset, self.transformed_queries)):
            ground_truth_urls = {self.normalize_url(url) for url in row.urls}
            
            retrieved_tests = self.retriever.invoke(
                transformed_query.rewritten_query
            )
            
            reranked_results = self.reranker.rerank(
                transformed_query.rewritten_query, 
                retrieved_tests
            )
            
            balanced_docs = self.balancer.balance_selection(
                reranked_results,
                transformed_query.preferred_intent
            )
            
            recommended_urls = {doc.metadata.get("url", "") for doc in balanced_docs}
            
            recall_k = len(recommended_urls.intersection(ground_truth_urls)) / len(ground_truth_urls)

            recalls.append(recall_k)
            self._log(f"Evaluate query {idx+1}/{len(self.dataset)}: Recall@K = {recall_k:.4f}")
        
        return sum(recalls) / len(recalls) if recalls else 0.0

    def normalize_url(self, url: str) -> str:
        """Normalize URL for comparison."""
        return url.strip().replace("https://www.shl.com/products", "https://www.shl.com/solutions/products")    
    