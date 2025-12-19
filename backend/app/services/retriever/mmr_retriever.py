from app.services.vector_store.factory import get_vector_store
from app.utils.envs import Envs


mmr_retriever = get_vector_store().as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": Envs.TOP_K,
        "fetch_k": Envs.FETCH_K,
        "lambda_mult": 1
    }
)
