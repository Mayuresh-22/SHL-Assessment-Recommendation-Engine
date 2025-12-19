import json
from langchain_core.language_models import BaseChatModel

from app.constants.strings import REWRITE_AND_INFER_SYS_PROMPT
from app.pydantic_models.data_model import PreferredIntent, TransformedQuery


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

        content = response.content if hasattr(response, "content") else response
        print("Query transformer raw LLM response:", content)

        try:
            parsed = json.loads(content.strip().replace("```json", "").replace("```", ""))  # type: ignore
        except json.JSONDecodeError:
            raise ValueError("LLM output is not valid JSON")

        return TransformedQuery(
            rewritten_query=parsed["rewritten_query"],
            preferred_intent=PreferredIntent(
                preferred_test_types=parsed["preferred_test_types"],
                duration_preference=parsed["duration_preference"]
            )
        )