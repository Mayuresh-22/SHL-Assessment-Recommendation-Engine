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
