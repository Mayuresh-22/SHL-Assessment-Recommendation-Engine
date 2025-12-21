from typing import Callable, List, Optional
from app.pydantic_models.data_model import DatasetRow, TransformedQuery
from langchain_core.retrievers import BaseRetriever


class EvalRetriever:
    
    def __init__(
        self, 
        retriever: BaseRetriever, 
        dataset: List[DatasetRow],
        transformed_queries: List[TransformedQuery],
        log_func: Optional[Callable[[str], None]] = None
    ):
        self.retriever = retriever
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
            
            retrieved_urls = {doc.metadata.get("url", "") for doc in retrieved_tests}
            
            recall_k = len(retrieved_urls.intersection(ground_truth_urls)) / len(ground_truth_urls)

            recalls.append(recall_k)
            self._log(f"Evaluate query {idx+1}/{len(self.dataset)}: Recall@K = {recall_k:.4f}")
        
        return sum(recalls) / len(recalls) if recalls else 0.0

    def normalize_url(self, url: str) -> str:
        """Normalize URL for comparison."""
        return url.strip().replace("https://www.shl.com/products", "https://www.shl.com/solutions/products")
