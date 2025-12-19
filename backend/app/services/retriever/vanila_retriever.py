from app.services.vector_store.factory import get_vector_store
from app.utils.envs import Envs


vanila_retriever = get_vector_store().as_retriever(
    search_type="similarity",
    search_kwargs={"k": Envs.TOP_K}
)
