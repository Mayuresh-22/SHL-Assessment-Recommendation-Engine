from collections import defaultdict
import os
from time import sleep
from typing import Dict, List
    
from app.services.query.query_transformer import QueryTransformer
from app.services.balancer.balancer import ResultBalancer
from app.pydantic_models.data_model import DatasetRow
from app.services.reranker.base_reranker import BaseReranker
from langchain_core.retrievers import BaseRetriever
from app.evaluation.eval_retriever import EvalRetriever
from app.evaluation.eval_reranker import EvalReranker


class Evaluator:
    """
    Final evaluator that runs both retriever and reranker+balancer evaluations.
    """
    
    def __init__(
        self, 
        retriever: BaseRetriever,
        query_transformer: QueryTransformer, 
        reranker: BaseReranker,
        balancer: ResultBalancer,
        dataset_file: str = "app/evaluation/dataset.xlsx",
        results_file: str = "eval_results.txt"
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.balancer = balancer
        self.query_transformer = query_transformer
        self.dataset_file = dataset_file
        self.results_file = results_file
        self._init_results_file()
        self.dataset = self.dataset_loader()
        self.transformed_queries = self.transform_all_queries()
    
    def _init_results_file(self):
        """Initialize/clear the results file."""
        with open(self.results_file, "w", encoding="utf-8") as f:
            f.write("")
    
    def _log(self, message: str = ""):
        """Write a message to the results file."""
        with open(self.results_file, "a", encoding="utf-8") as f:
            f.write(message + "\n")
    
    def dataset_loader(self) -> List[DatasetRow]:
        self._log(f"Loading dataset from {self.dataset_file}...")
        import pandas as pd
        df = pd.read_excel(self.dataset_file, sheet_name="Train-Set")
        
        temp_dataset = defaultdict(set)
        for _, row in df.iterrows():
            temp_dataset[row["Query"]].add(row["Assessment_url"])
        
        dataset: List[DatasetRow] = []
        for query, urls in temp_dataset.items():
            dataset.append(DatasetRow(query=query, urls=urls))

        self._log(f"Loaded {len(dataset)} queries from the dataset.")
        return dataset
    
    def transform_all_queries(self):
        """Transform all queries in the dataset."""
        self._log("Transforming all queries in the dataset...")
        transformed_queries = []
        for row in self.dataset:
            transformed_query = self.query_transformer.rewrite_and_infer(row.query)
            transformed_queries.append(transformed_query)
        self._log("All queries transformed.")
        return transformed_queries
    
    def evaluate_retriever(self) -> float:
        """Evaluate the retriever only."""
        self._log("\n" + "="*50)
        self._log("EVALUATING RETRIEVER")
        self._log("="*50)
        
        eval_retriever = EvalRetriever(
            retriever=self.retriever,
            dataset=self.dataset,
            transformed_queries=self.transformed_queries,
            log_func=self._log
        )
        recall = eval_retriever.evaluate()
        self._log(f"\nRetriever Average Recall@K: {recall:.4f}")
        return recall
    
    def evaluate_reranker(self) -> float:
        """Evaluate the full pipeline (retriever + reranker + balancer)."""
        if self.reranker is None:
            raise ValueError("Reranker not provided. Cannot evaluate reranker.")
        if self.balancer is None:
            raise ValueError("Balancer not provided. Cannot evaluate reranker.")
        
        self._log("\n" + "="*50)
        self._log("EVALUATING RERANKER + BALANCER PIPELINE")
        self._log("="*50)
        
        eval_reranker = EvalReranker(
            retriever=self.retriever,
            reranker=self.reranker,
            balancer=self.balancer,
            dataset=self.dataset,
            transformed_queries=self.transformed_queries,
            log_func=self._log
        )
        recall = eval_reranker.evaluate()
        self._log(f"\nReranker+Balancer Average Recall@K: {recall:.4f}")
        return recall
    
    def evaluate_all(self) -> Dict[str, float]:
        """
        Run both retriever and reranker+balancer evaluations.
        Returns a dictionary with results.
        """
        results = {}
        
        print("Evaluation started, check eval_results.txt for progress...")
        results["retriever_recall"] = self.evaluate_retriever()
        
        if self.reranker is not None and self.balancer is not None:
            results["pipeline_recall"] = self.evaluate_reranker()
        
        self._log("\n" + "="*50)
        self._log("EVALUATION SUMMARY")
        self._log("="*50)
        self._log(f"Retriever Recall@K:          {results['retriever_recall']:.4f}")
        if "pipeline_recall" in results:
            self._log(f"Reranker+Balancer Recall@K:  {results['pipeline_recall']:.4f}")
        self._log("="*50)
        
        print(f"Evaluation complete. Please see the results in '{self.results_file}'")
        
        return results
