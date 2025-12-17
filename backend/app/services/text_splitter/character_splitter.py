from langchain_text_splitters import CharacterTextSplitter


character_splitter = CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separator="\n\n",
    length_function=len,
)
