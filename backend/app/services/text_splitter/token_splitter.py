from langchain_text_splitters import TokenTextSplitter


token_splitter = TokenTextSplitter(
    chunk_size=256,  # tokens, not characters
    chunk_overlap=20,
)
