from typing import List
from pydantic import BaseModel


class IndividualTest(BaseModel):
    page_content: str
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
