import os
from app.utils.envs import Envs


from langchain_google_genai import GoogleGenerativeAIEmbeddings

os.environ["GOOGLE_API_KEY"] = Envs.GOOGLE_API_KEY
google_embedder = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    task_type="SEMANTIC_SIMILARITY"
)