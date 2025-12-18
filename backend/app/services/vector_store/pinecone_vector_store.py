import time
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from app.utils.envs import Envs
from app.services.embedder.factory import get_embedder

pc = Pinecone(api_key=Envs.PINECONE_API_KEY)
index_name = Envs.PINECONE_INDEX_NAME

if not pc.has_index(index_name):
    print("Creating Pinecone index...")
    pc.create_index(
        name=index_name,
        dimension=get_embedder()["dimension"],
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    while not pc.describe_index(index_name).status["ready"]:
        time.sleep(1)
    print("Created Pinecone index.")

index = pc.Index(index_name)

pinecone_vector_store = PineconeVectorStore(
    embedding=get_embedder()["embedder"], 
    index=index
)
