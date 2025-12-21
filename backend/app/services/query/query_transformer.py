import json
from langchain_core.language_models import BaseChatModel

from app.constants.strings import REWRITE_AND_INFER_SYS_PROMPT
from app.pydantic_models.data_model import LLMStructuredOutput, PreferredIntent, TransformedQuery


class QueryTransformer:
    
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
    
    def rewrite_and_infer(self, query: str) -> TransformedQuery:
        response = self.llm.invoke(
            [
                {"role": "system", "content": REWRITE_AND_INFER_SYS_PROMPT},
                {"role": "user", "content": query}
            ]
        )

        content: LLMStructuredOutput = response.content if hasattr(response, "content") else response  # type: ignore

        return TransformedQuery(
            rewritten_query=content.rewritten_query,
            preferred_intent=PreferredIntent(
                preferred_test_types=content.preferred_test_types,
                duration_preference=content.duration_preference
            )
        )