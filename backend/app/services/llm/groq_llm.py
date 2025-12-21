import os
from langchain_groq import ChatGroq
from app.pydantic_models.data_model import LLMStructuredOutput
from app.utils.envs import Envs


os.environ["GROQ_API_KEY"] = Envs.GROQ_API_KEY
groq_llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0.7, max_retries=3)
groq_llm = groq_llm.with_structured_output(LLMStructuredOutput)
