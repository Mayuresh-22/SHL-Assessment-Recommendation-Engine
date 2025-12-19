import os
from langchain_groq import ChatGroq
from app.utils.envs import Envs


os.environ["GROQ_API_KEY"] = Envs.GROQ_API_KEY
groq_llm = ChatGroq(model="llama-3.3-70b-versatile")
