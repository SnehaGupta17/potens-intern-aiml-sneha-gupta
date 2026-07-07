from langchain_chroma import Chroma
from src.embeddings import get_embedding_model

DB_PATH = "data/chroma_db"


def create_vector_store(chunks):

    embeddings = get_embedding_model()

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    print(f"\nStored {len(chunks)} chunks in ChromaDB")

    return vector_store