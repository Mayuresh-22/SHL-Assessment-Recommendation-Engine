import os
from langchain.chat_models import init_chat_model
from app.pydantic_models.data_model import LLMStructuredOutput
from app.utils.envs import Envs


os.environ["GOOGLE_API_KEY"] = Envs.GOOGLE_API_KEY
google_llm = init_chat_model("google_genai:gemini-2.5-flash-lite")
google_llm = google_llm.with_structured_output(LLMStructuredOutput)
