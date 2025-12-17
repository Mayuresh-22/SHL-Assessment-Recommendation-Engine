from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from app.utils.envs import Envs
from app.services.embedder.factory import get_embedder

pc = Pinecone(api_key=Envs.PINECONE_API_KEY)
index = pc.Index(Envs.PINECONE_INDEX_NAME)

pinecone_vector_store = PineconeVectorStore(embedding=get_embedder(), index=index)
