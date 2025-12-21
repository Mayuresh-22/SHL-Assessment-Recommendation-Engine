from typing import List, Optional, Set
from pydantic import BaseModel, Field


class IndividualTest(BaseModel):
    page_content: Optional[str] = Field(None, exclude=True)
    url: str
    name: str
    description: str
    duration: int
    remote_support: bool
    adaptive_support: bool
    test_type: List[str]


class PreferredIntent(BaseModel):
    preferred_test_types: List[str]
    duration_preference: str | None


class TransformedQuery(BaseModel):
    rewritten_query: str
    preferred_intent: PreferredIntent


class LLMStructuredOutput(BaseModel):
    rewritten_query: str
    preferred_test_types: List[str]
    duration_preference: Optional[str]


class DatasetRow(BaseModel):
    query: str
    urls: Set[str]
