from langchain_chroma import Chroma
from src.embeddings import get_embedding_model

DB_PATH = "data/chroma_db"


def get_retriever():
    embeddings = get_embedding_model()

    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )

    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

    return retriever