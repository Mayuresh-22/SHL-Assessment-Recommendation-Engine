from pprint import pprint
from typing import List
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document

from app.pydantic_models.data_model import IndividualTest
from app.services.balancer.balancer import ResultBalancer
from app.services.query.query_transformer import QueryTransformer
from app.services.reranker.base_reranker import BaseReranker


class Recommender:
    """
    This class is responsible for orchestrating the recommendation process,
    like query tranformation, doc retrieval, reranking,
    and provide balanced assessment recommendation based on user query.
    """
    def __init__(
        self, 
        query_transformer: QueryTransformer, 
        retriever: BaseRetriever, 
        reranker: BaseReranker, 
        balancer: ResultBalancer
    ):
        self.query_transformer = query_transformer
        self.retriever = retriever
        self.reranker = reranker
        self.balancer = balancer
    
    def recommend(self, user_query: str) -> List[Document]:
        print("User Query transforming...")
        transformed_query = self.query_transformer.rewrite_and_infer(user_query)
        print("Transformed Query:", transformed_query, ", retrieving tests...")
        retrieved_tests = self.retriever.invoke(
            transformed_query.rewritten_query
        )
        print(f"Retrieved {len(retrieved_tests)} tests, reranking...")
        reranked_tests = self.reranker.rerank(
            transformed_query.rewritten_query,
            retrieved_tests
        )
        print(f"Reranked {len(reranked_tests)} tests, displaying...")
        balanced_tests = self.balancer.balance_selection(
            reranked_tests,
            transformed_query.preferred_intent
        )
        
        return balanced_tests
