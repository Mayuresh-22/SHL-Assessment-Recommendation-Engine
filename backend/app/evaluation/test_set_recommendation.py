# This script generates the submission CSV file that contains predictions for unlabeled test set.
from typing import List

from app.services.query.query_transformer import QueryTransformer
from app.services.balancer.balancer import ResultBalancer
from app.services.reranker.base_reranker import BaseReranker
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

class TestSetRecommendation:
    def __init__(
        self,
        retriever: BaseRetriever,
        reranker: BaseReranker,
        balancer: ResultBalancer,
        query_transformer: QueryTransformer,
        dataset_file: str = "app/evaluation/dataset.xlsx",
        results_file: str = "test_set_predictions.csv"
    ):
        self.retriever = retriever
        self.reranker = reranker
        self.balancer = balancer
        self.query_transformer = query_transformer
        self.dataset_file = dataset_file
        self.results_file = results_file
        self.dataset = self.dataset_loader()
        self.transformed_queries = self.transform_all_queries()
    
    def dataset_loader(self) -> List[str]:
        print(f"Loading dataset from {self.dataset_file}...")
        import pandas as pd
        df = pd.read_excel(self.dataset_file, sheet_name="Test-Set")
        
        test_queries = []
        for _, row in df.iterrows():
            test_queries.append(row["Query"])

        print(f"Loaded {len(test_queries)} queries from the dataset.")
        return test_queries
    
    def transform_all_queries(self):
        """Transform all queries in the dataset."""
        print("Transforming all queries in the dataset...")
        transformed_queries = []
        for query in self.dataset:
            transformed_query = self.query_transformer.rewrite_and_infer(query)
            transformed_queries.append(transformed_query)
        print("All queries transformed.")
        return transformed_queries
    
    def generate_recommendations(self) -> List[List[Document]]:
        print("Generating recommendations for the test set...")
        all_retrieved_results: List[List[Document]] = []
        
        for query in self.transformed_queries:
            retrieved_tests = self.retriever.invoke(
                query.rewritten_query
            )
            reranked_tests = self.reranker.rerank(
                query.rewritten_query,
                retrieved_tests
            )
            balanced_tests = self.balancer.balance_selection(
                reranked_tests,
                query.preferred_intent
            )
            all_retrieved_results.append(balanced_tests)  # type: ignore
        
        return all_retrieved_results
    
    def save_recommendations(self, recommendations: List[List[Document]]):
        print(f"Saving recommendations to {self.results_file}...")
        import csv
        
        with open(self.results_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Query", "Assessment_url"])
            
            for idx, query in enumerate(self.dataset):
                recs = recommendations[idx]
                for rec in recs:
                    writer.writerow([query, rec.metadata.get("url", "N/A")])
        
        print("Recommendations saved successfully.")
    
    def run(self):
        recommendations = self.generate_recommendations()
        self.save_recommendations(recommendations)
