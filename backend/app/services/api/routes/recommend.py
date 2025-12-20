from typing import List
from fastapi import APIRouter
from groq import BaseModel
from langchain_classic.retrievers.contextual_compression import (
    ContextualCompressionRetriever,
)
from pydantic import Field

from app.pydantic_models.data_model import IndividualTest
from app.services.balancer.balancer import ResultBalancer
from app.services.llm.factory import get_llm
from app.services.query.query_transformer import QueryTransformer
from app.services.recommender.recommender import Recommender
from app.services.reranker.factory import get_reranker
from app.services.retriever.factory import get_retriever


class Body(BaseModel):
    query: str = Field(..., min_length=1, max_length=5000)


router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/")
def recommend(body: Body) -> List[IndividualTest]:
    
    recommender = Recommender(
        query_transformer=QueryTransformer(llm=get_llm()),
        retriever=ContextualCompressionRetriever(
            base_compressor=get_reranker().get_compressor(), base_retriever=get_retriever()
        ),
        reranker=get_reranker(),
        balancer=ResultBalancer()
    )
    
    recommendations = recommender.recommend(body.query)
    
    recommended_tests = []
    for idx, doc in enumerate(recommendations, start=1):
        del doc.metadata["relevance_score"]
        recommended_tests.append(
            IndividualTest(**doc.metadata)
        )
    
    return recommended_tests
