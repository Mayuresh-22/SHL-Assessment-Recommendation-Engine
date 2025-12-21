from typing import Dict, List
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
from app.services.scraper.assessment_scraper import TEST_TYPE_MAP


class Body(BaseModel):
    query: str = Field(..., min_length=1)


router = APIRouter(prefix="/recommend", tags=["Recommendations"])

@router.post("/")
def recommend(body: Body):
    
    recommender = Recommender(
        query_transformer=QueryTransformer(llm=get_llm()),
        retriever=get_retriever(),
        reranker=get_reranker(),
        balancer=ResultBalancer()
    )
    
    recommendations = recommender.recommend(body.query)
    
    recommended_tests = []
    for idx, doc in enumerate(recommendations, start=1):
        del doc.metadata["relevance_score"]
        doc.metadata["test_type"] = [TEST_TYPE_MAP[test_type] for test_type in doc.metadata.get("test_type", [])]
        doc.metadata["adaptive_support"] = "Yes" if doc.metadata.get("adaptive_support", False) else "No"
        doc.metadata["remote_support"] = "Yes" if doc.metadata.get("remote_support", False) else "No"
        recommended_tests.append(
            doc.metadata
        )
    
    return {
        "recommended_assessments": recommended_tests
    }
